#!/usr/bin/env python3
"""
Read github-repository.txt (see github-repository.py) and, for every listed
repository whose folder is missing from the parent directory, `git clone` it
there. Repositories that already have a local folder are left untouched.

Requires the `git` executable to be available on PATH; no third-party Python
package is used. SSH clone URLs rely on the system's own SSH key/agent setup
for GitHub authentication (no token needed by this script).
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_ENV_FILE = ".env"
DEFAULT_REPOSITORY_LIST_FILE = "github-repository.txt"
DEFAULT_TARGET_DIR = ".."

ENV_KEYS = (
    "GITHUB_REPOSITORY_LIST_FILE",
    "GITHUB_CLONE_TARGET_DIR",
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


def clone_repo(url: str, target_dir: Path) -> bool:
    try:
        result = subprocess.run(["git", "clone", url, str(target_dir)])
    except FileNotFoundError as e:
        raise RuntimeError("'git' executable not found on PATH; it is required to clone repositories.") from e

    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clone every repository listed in github-repository.txt that is missing locally."
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
        help=f"Directory to clone missing repositories into (default: value from .env, or {DEFAULT_TARGET_DIR}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List repositories that would be cloned, without actually cloning them.",
    )
    args = parser.parse_args()

    config = load_config(Path(args.env_file))

    list_file = args.input or config.get("GITHUB_REPOSITORY_LIST_FILE", DEFAULT_REPOSITORY_LIST_FILE)
    target_dir_str = args.dir or config.get("GITHUB_CLONE_TARGET_DIR", DEFAULT_TARGET_DIR)

    list_path = Path(list_file)
    target_dir = Path(target_dir_str)

    try:
        entries = load_repository_list(list_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    missing = [entry for entry in entries if not (target_dir / entry["repo"]).is_dir()]

    if not missing:
        print(f"Checked {len(entries)} repositories, nothing to clone.")
        return 0

    if args.dry_run:
        for entry in missing:
            print(f"Would clone {entry['url']} -> {target_dir / entry['repo']}")
        print(f"{len(missing)} of {len(entries)} repositories would be cloned.")
        return 0

    cloned, failed = 0, 0
    for entry in missing:
        repo_dir = target_dir / entry["repo"]
        print(f"Cloning {entry['url']} -> {repo_dir}")
        try:
            ok = clone_repo(entry["url"], repo_dir)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

        if ok:
            cloned += 1
        else:
            failed += 1
            print(f"Error: failed to clone {entry['url']}", file=sys.stderr)

    print(f"Cloned {cloned} repositories, {failed} failed, {len(entries) - len(missing)} already present.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
