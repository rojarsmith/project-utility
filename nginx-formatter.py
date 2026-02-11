#!/usr/bin/env python3
"""
Nginx config formatter tool (auto-venv bootstrap).

Features:
- Auto create/use .venv
- Auto install nginxfmt inside .venv
- Format nginx config from file or stdin
- Configurable indentation spaces
- Output to stdout or write back (in-place), optional backup
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

VENV_DIR = Path(".venv")
PKG_NAME = "nginxfmt"


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

    # 2) Ensure package installed
    try:
        subprocess.check_call(
            [str(py), "-c", "import nginxfmt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print(f"📦 Installing {PKG_NAME} in .venv ...")
        subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(py), "-m", "pip", "install", PKG_NAME])

    # 3) Re-exec current script with venv python
    os.execv(str(py), [str(py), *sys.argv])


def read_text(path: Path) -> str:
    # Read file as text; assume utf-8, fallback to latin1
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def write_text(path: Path, text: str) -> None:
    # Write file as utf-8 (nginx config is typically ascii/utf-8)
    path.write_text(text, encoding="utf-8")


def format_text(text: str, indent: int, line_endings: str) -> str:
    import nginxfmt

    fo = nginxfmt.FormatterOptions()
    fo.indentation = int(indent)

    # line_endings: "auto" means keep default behavior; otherwise force
    # nginxfmt expects '\n' or '\r\n' (per docs/examples)
    if line_endings == "lf":
        fo.line_endings = "\n"
    elif line_endings == "crlf":
        fo.line_endings = "\r\n"

    formatter = nginxfmt.Formatter(fo)
    return formatter.format_string(text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format/beautify Nginx config with configurable indentation (auto-venv)."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file path. Use '-' or omit to read from stdin.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="Output file path. Use '-' for stdout (default). Ignored if --in-place is set.",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=4,
        help="Number of spaces for indentation (default: 4).",
    )
    parser.add_argument(
        "--line-endings",
        choices=["auto", "lf", "crlf"],
        default="auto",
        help="Line endings style: auto/lf/crlf (default: auto).",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file with formatted content (input must be a file path).",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="When used with --in-place, create a backup file with suffix '~'.",
    )

    args = parser.parse_args()

    # Read input
    if args.input == "-" or args.input is None:
        raw = sys.stdin.read()
        input_path = None
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_path}", file=sys.stderr)
            return 2
        raw = read_text(input_path)

    # Format
    formatted = format_text(raw, args.indent, args.line_endings)

    # Write output
    if args.in_place:
        if input_path is None:
            print("❌ --in-place requires an input file path (not stdin).", file=sys.stderr)
            return 2
        if args.backup:
            backup_path = input_path.with_name(input_path.name + "~")
            backup_path.write_bytes(input_path.read_bytes())
        write_text(input_path, formatted)
        return 0

    # Output to file or stdout
    if args.output == "-" or args.output is None:
        sys.stdout.write(formatted)
    else:
        out_path = Path(args.output)
        write_text(out_path, formatted)

    return 0


if __name__ == "__main__":
    ensure_venv_and_reexec()
    raise SystemExit(main())
