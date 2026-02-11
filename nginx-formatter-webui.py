#!/usr/bin/env python3
"""
Local Web UI for formatting Nginx config (auto-venv bootstrap).

- Auto create/use .venv
- Auto install Flask + nginxfmt in .venv
- Starts a local web server and opens browser
- Paste nginx config -> format -> copy to clipboard (browser JS)
"""

import os
import sys
import subprocess
from pathlib import Path


VENV_DIR = Path(".venv")
REQUIREMENTS = ["flask>=2.0", "nginxfmt>=0.5"]  # minimal, can be pinned if needed
HOST = "127.0.0.1"
PORT = 8787


def venv_python() -> Path:
    # Return the venv python path for Windows or POSIX
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_venv_and_reexec() -> None:
    # If already running inside venv, do nothing
    if sys.prefix != sys.base_prefix:
        return

    py = venv_python()

    # 1) Create venv if missing
    if not py.exists():
        print("🐍 Creating venv at .venv ...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

    # 2) Ensure requirements installed
    def _has_all_pkgs() -> bool:
        try:
            subprocess.check_call(
                [str(py), "-c", "import flask, nginxfmt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    if not _has_all_pkgs():
        print("📦 Installing dependencies in .venv ...")
        subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(py), "-m", "pip", "install", *REQUIREMENTS])

    # 3) Re-exec current script with venv python
    os.execv(str(py), [str(py), *sys.argv])


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Nginx Formatter (Local)</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 18px; }
    .row { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    textarea { width: 100%; min-height: 240px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-size: 13px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
    button { padding: 8px 12px; cursor: pointer; }
    select, input { padding: 6px 8px; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 12px; }
    .muted { color: #666; font-size: 12px; }
    .status { margin-left: 8px; font-size: 12px; }
  </style>
</head>
<body>
  <h2>Nginx Config Formatter (Local Web UI)</h2>
  <div class="muted">Paste your nginx config, choose indentation, click Format, then Copy.</div>

  <div class="row" style="margin: 12px 0;">
    <label>Indent spaces:
      <select id="indent">
        <option>2</option>
        <option selected>4</option>
        <option>8</option>
      </select>
    </label>

    <label>Line endings:
      <select id="line_endings">
        <option value="auto" selected>auto</option>
        <option value="lf">lf</option>
        <option value="crlf">crlf</option>
      </select>
    </label>

    <button id="btnFormat">Format</button>
    <button id="btnCopy" disabled>Copy output</button>
    <span class="status" id="status"></span>
  </div>

  <div class="grid">
    <div class="card">
      <div><strong>Input</strong></div>
      <textarea id="input" placeholder="Paste nginx config here..."></textarea>
    </div>
    <div class="card">
      <div><strong>Output</strong></div>
      <textarea id="output" placeholder="Formatted result appears here..." readonly></textarea>
    </div>
  </div>

<script>
  const $ = (id) => document.getElementById(id);
  const setStatus = (msg) => { $("status").textContent = msg || ""; };

  $("btnFormat").addEventListener("click", async () => {
    setStatus("Formatting...");
    $("btnCopy").disabled = true;
    $("output").value = "";

    const payload = {
      text: $("input").value,
      indent: parseInt($("indent").value, 10),
      line_endings: $("line_endings").value
    };

    try {
      const res = await fetch("/api/format", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Request failed");

      $("output").value = data.formatted || "";
      $("btnCopy").disabled = !$("output").value;
      setStatus("Done.");
    } catch (e) {
      setStatus("Error: " + e.message);
    }
  });

  $("btnCopy").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($("output").value || "");
      setStatus("Copied to clipboard.");
    } catch (e) {
      // Fallback for older browsers
      $("output").focus();
      $("output").select();
      document.execCommand("copy");
      setStatus("Copied (fallback).");
    }
  });
</script>
</body>
</html>
"""


def format_nginx(text: str, indent: int, line_endings: str) -> str:
    # Format nginx config using nginxfmt
    import nginxfmt

    fo = nginxfmt.FormatterOptions()
    fo.indentation = int(indent)

    # nginxfmt uses '\n' or '\r\n' when line_endings is set
    if line_endings == "lf":
        fo.line_endings = "\n"
    elif line_endings == "crlf":
        fo.line_endings = "\r\n"

    formatter = nginxfmt.Formatter(fo)
    return formatter.format_string(text or "")


def run_server():
    # Start Flask server
    from flask import Flask, request, jsonify
    import threading
    import webbrowser
    import time

    app = Flask(__name__)

    @app.get("/")
    def index():
        return HTML, 200, {"Content-Type": "text/html; charset=utf-8"}

    @app.post("/api/format")
    def api_format():
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        indent = data.get("indent", 4)
        line_endings = data.get("line_endings", "auto")

        if not isinstance(indent, int) or indent < 0 or indent > 16:
            return jsonify(error="Indent must be an integer between 0 and 16."), 400
        if line_endings not in ("auto", "lf", "crlf"):
            return jsonify(error="Invalid line_endings."), 400

        try:
            formatted = format_nginx(text, indent, line_endings)
            return jsonify(formatted=formatted)
        except Exception as e:
            return jsonify(error=str(e)), 500

    # Open browser shortly after server starts
    def _open_browser():
        time.sleep(0.6)
        url = f"http://{HOST}:{PORT}/"
        try:
            webbrowser.open(url, new=1, autoraise=True)
        except Exception:
            pass

    threading.Thread(target=_open_browser, daemon=True).start()

    print(f"🌐 Web UI running at http://{HOST}:{PORT}/")
    print("Press Ctrl+C to stop.")
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    ensure_venv_and_reexec()
    run_server()
