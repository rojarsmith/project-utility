#!/usr/bin/env python3
"""
Read github-repository.txt (see github-repository.py) and, for every listed
repository that has a matching local folder in the parent directory, run
`git pull` there. Repositories with no local folder are skipped (use
github-clone.py to fetch them first). Writes a plain-text pull report to
github-pull.txt, including the reason for any failed pull (local
modifications, merge conflicts, etc.).

Requires the `git` executable to be available on PATH; no third-party Python
package is used.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

DEFAULT_ENV_FILE = ".env"
DEFAULT_REPOSITORY_LIST_FILE = "github-repository.txt"
DEFAULT_TARGET_DIR = ".."
DEFAULT_REPORT_FILE = "github-pull.txt"
MAX_DETAIL_LENGTH = 500

ENV_KEYS = (
    "GITHUB_REPOSITORY_LIST_FILE",
    "GITHUB_PULL_TARGET_DIR",
    "GITHUB_PULL_REPORT_FILE",
)

REPO_URL_RE = re.compile(
    r"^(?:git@[^:]+:|https?://[^/]+/)(?P<owner>[^/]+)/(?P<repo>.+?)(?:\.git)?/?$"
)


def load_env_file(env_path: Path) -> dict:
    # Minimal KEY=VALUE parser: skips blank lines/comments, strips an optional
    # "export " prefix and matching surrounding quotes. No external dependency.
    values = {}
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        if "=" not in line:
            continue

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        values[key] = value

    return values


def load_config(env_path: Path) -> dict:
    config = load_env_file(env_path)
    # Real environment variables override the .env file
    for key in ENV_KEYS:
        if key in os.environ:
            config[key] = os.environ[key]
    return config


def parse_repo_url(url: str):
    match = REPO_URL_RE.match(url.strip())
    if not match:
        return None
    return match.group("owner"), match.group("repo")


def load_repository_list(list_path: Path) -> list:
    if not list_path.exists():
        raise FileNotFoundError(f"Repository list file not found: {list_path}")

    entries = []
    lines = list_path.read_text(encoding="utf-8").splitlines()
    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split(None, 1)
        if len(parts) != 2:
            print(f"Warning: skipping malformed line {line_no} in {list_path}: {raw_line!r}", file=sys.stderr)
            continue

        visibility, url = parts
        parsed = parse_repo_url(url)
        if not parsed:
            print(f"Warning: could not parse repo URL on line {line_no}: {url!r}", file=sys.stderr)
            continue

        owner, repo = parsed
        entries.append({"visibility": visibility, "url": url, "owner": owner, "repo": repo})

    return entries


def pull_repo(repo_dir: Path) -> tuple:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "pull"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as e:
        raise RuntimeError("'git' executable not found on PATH; it is required to pull repositories.") from e

    return result.returncode, result.stdout, result.stderr


def summarize_output(stdout: str, stderr: str) -> str:
    # Collapse git's (possibly multi-line, multi-stream) output into one line
    # so each repo still takes a single row in the report.
    lines = [line.strip() for line in (stdout + "\n" + stderr).splitlines() if line.strip()]
    summary = " | ".join(lines)
    if len(summary) > MAX_DETAIL_LENGTH:
        summary = summary[:MAX_DETAIL_LENGTH].rstrip() + "..."
    return summary


def check_entry(target_dir: Path, entry: dict) -> dict:
    repo_dir = target_dir / entry["repo"]

    if not repo_dir.is_dir():
        return {**entry, "status": "MISSING", "detail": "no local folder, nothing to pull"}

    if not (repo_dir / ".git").exists():
        return {**entry, "status": "NOT_A_GIT_REPO", "detail": "folder exists but is not a git repository"}

    returncode, stdout, stderr = pull_repo(repo_dir)
    detail = summarize_output(stdout, stderr) or "(no output)"

    if returncode != 0:
        return {**entry, "status": "FAILED", "detail": detail}

    return {**entry, "status": "OK", "detail": detail}


def build_report(results: list, list_path: Path, target_dir: Path) -> str:
    lines = [
        "GitHub Pull Report",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source list: {list_path} ({len(results)} entries)",
        f"Target directory: {target_dir}",
        "",
    ]

    status_width = max((len(r["status"]) for r in results), default=0)
    repo_width = max((len(r["repo"]) for r in results), default=0)
    for r in results:
        label = f"[{r['status']}]".ljust(status_width + 2)
        lines.append(f"{label} {r['repo']:<{repo_width}} {r['detail']}")

    counts = Counter(r["status"] for r in results)
    summary = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))

    lines.append("")
    lines.append(f"Summary: {summary}" if summary else "Summary: nothing to check")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pull every repository listed in github-repository.txt that exists locally."
    )
    parser.add_argument(
        "-e",
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help=f"Path to the .env parameter file (default: {DEFAULT_ENV_FILE}).",
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help=f"Path to the repository list file (default: value from .env, or {DEFAULT_REPOSITORY_LIST_FILE}).",
    )
    parser.add_argument(
        "-d",
        "--dir",
        default=None,
        help=f"Directory containing the local repo folders (default: value from .env, or {DEFAULT_TARGET_DIR}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=f"Pull report output file path (default: value from .env, or {DEFAULT_REPORT_FILE}).",
    )
    args = parser.parse_args()

    config = load_config(Path(args.env_file))

    list_file = args.input or config.get("GITHUB_REPOSITORY_LIST_FILE", DEFAULT_REPOSITORY_LIST_FILE)
    target_dir_str = args.dir or config.get("GITHUB_PULL_TARGET_DIR", DEFAULT_TARGET_DIR)
    report_file = args.output or config.get("GITHUB_PULL_REPORT_FILE", DEFAULT_REPORT_FILE)

    list_path = Path(list_file)
    target_dir = Path(target_dir_str)

    try:
        entries = load_repository_list(list_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    results = []
    try:
        for entry in entries:
            print(f"Pulling {entry['repo']} ...")
            results.append(check_entry(target_dir, entry))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    report = build_report(results, list_path, target_dir)

    report_path = Path(report_file)
    report_path.write_text(report, encoding="utf-8")

    failed = sum(1 for r in results if r["status"] == "FAILED")
    print(f"Checked {len(results)} repositories, {failed} failed.")
    print(f"Report saved to: {report_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
