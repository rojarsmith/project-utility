#!/usr/bin/env python3
"""
Check that every repository listed in github-repository.txt (see
github-repository.py) has a matching local clone in the parent directory, and
flag local git repos that are not in the list. Writes a plain-text report to
github-integrity.txt.

Requires the `git` executable to be available on PATH (already a prerequisite
for cloning the repos in the first place); no third-party Python package is used.
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
DEFAULT_REPORT_FILE = "github-integrity.txt"
DEFAULT_PARENT_DIR = ".."

ENV_KEYS = (
    "GITHUB_REPOSITORY_LIST_FILE",
    "GITHUB_INTEGRITY_REPORT_FILE",
    "GITHUB_INTEGRITY_PARENT_DIR",
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


def get_git_remote_url(repo_dir: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as e:
        raise RuntimeError("'git' executable not found on PATH; it is required to verify local clones.") from e

    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def check_entry(parent_dir: Path, entry: dict) -> dict:
    repo_dir = parent_dir / entry["repo"]

    if not repo_dir.is_dir():
        return {**entry, "status": "MISSING", "detail": "no local folder"}

    if not (repo_dir / ".git").exists():
        return {**entry, "status": "NOT_A_GIT_REPO", "detail": "folder exists but is not a git repository"}

    remote_url = get_git_remote_url(repo_dir)
    if not remote_url:
        return {**entry, "status": "NO_REMOTE", "detail": "git repository has no 'origin' remote"}

    parsed = parse_repo_url(remote_url)
    if not parsed or parsed[0].lower() != entry["owner"].lower() or parsed[1].lower() != entry["repo"].lower():
        return {**entry, "status": "REMOTE_MISMATCH", "detail": f"local remote is {remote_url}"}

    return {**entry, "status": "OK", "detail": remote_url}


def find_extra_dirs(parent_dir: Path, expected_repo_names: set) -> list:
    extras = []
    if not parent_dir.is_dir():
        return extras

    for child in sorted(parent_dir.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name in expected_repo_names:
            continue
        if not (child / ".git").exists():
            continue

        remote_url = get_git_remote_url(child)
        extras.append({"name": child.name, "remote": remote_url or "(no origin remote)"})

    return extras


def build_report(results: list, extras: list, list_path: Path, parent_dir: Path) -> str:
    lines = [
        "GitHub Clone Integrity Report",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source list: {list_path} ({len(results)} entries)",
        f"Scanned directory: {parent_dir}",
        "",
    ]

    status_width = max((len(r["status"]) for r in results), default=0)
    repo_width = max((len(r["repo"]) for r in results), default=0)
    for r in results:
        label = f"[{r['status']}]".ljust(status_width + 2)
        lines.append(f"{label} {r['repo']:<{repo_width}} {r['detail']}")

    if extras:
        lines.append("")
        lines.append("Extra local git repositories not listed in the repository list:")
        extra_width = max(len(e["name"]) for e in extras)
        for e in extras:
            lines.append(f"[EXTRA] {e['name']:<{extra_width}} remote: {e['remote']}")

    counts = Counter(r["status"] for r in results)
    summary_parts = [f"{count} {status}" for status, count in sorted(counts.items())]
    if extras:
        summary_parts.append(f"{len(extras)} EXTRA")

    lines.append("")
    lines.append("Summary: " + (", ".join(summary_parts) if summary_parts else "nothing to check"))

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify local clones against github-repository.txt and report missing/extra directories."
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
        help=f"Directory to scan for local clones (default: value from .env, or {DEFAULT_PARENT_DIR}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=f"Report output file path (default: value from .env, or {DEFAULT_REPORT_FILE}).",
    )
    args = parser.parse_args()

    config = load_config(Path(args.env_file))

    list_file = args.input or config.get("GITHUB_REPOSITORY_LIST_FILE", DEFAULT_REPOSITORY_LIST_FILE)
    report_file = args.output or config.get("GITHUB_INTEGRITY_REPORT_FILE", DEFAULT_REPORT_FILE)
    parent_dir_str = args.dir or config.get("GITHUB_INTEGRITY_PARENT_DIR", DEFAULT_PARENT_DIR)

    list_path = Path(list_file)
    parent_dir = Path(parent_dir_str)

    try:
        entries = load_repository_list(list_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    try:
        results = [check_entry(parent_dir, entry) for entry in entries]
        extras = find_extra_dirs(parent_dir, {entry["repo"] for entry in entries})
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    report = build_report(results, extras, list_path, parent_dir)

    report_path = Path(report_file)
    report_path.write_text(report, encoding="utf-8")

    print(f"Checked {len(results)} repositories, found {len(extras)} extra local repo(s).")
    print(f"Report saved to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
