#!/usr/bin/env python3
"""
Fetch all GitHub repositories (public and private) for the authenticated user
via the GitHub REST API, and save their SSH clone URLs to a text file.

Each output line is formatted as: "<public|private> <ssh_clone_url>"

Uses only the Python standard library (urllib), no extra dependency required.
Parameters are read from a .env file; real OS environment variables (e.g. in CI)
take precedence over the .env file so secrets never need to touch disk there.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_ENV_FILE = ".env"
DEFAULT_OUTPUT_FILE = "github-clone.txt"
DEFAULT_API_BASE_URL = "https://api.github.com"
DEFAULT_PER_PAGE = 100
DEFAULT_AFFILIATION = "owner"

ENV_KEYS = (
    "GITHUB_TOKEN",
    "GITHUB_USERNAME",
    "GITHUB_API_BASE_URL",
    "GITHUB_OUTPUT_FILE",
    "GITHUB_PER_PAGE",
    "GITHUB_AFFILIATION",
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


def parse_link_header(header_value: str) -> dict:
    # Parse GitHub's pagination "Link" header into a {rel: url} mapping
    links = {}
    if not header_value:
        return links
    for part in header_value.split(","):
        segments = part.split(";")
        if len(segments) < 2:
            continue
        url = segments[0].strip().strip("<>")
        rel = None
        for seg in segments[1:]:
            seg = seg.strip()
            if seg.startswith("rel="):
                rel = seg.split("=", 1)[1].strip('"')
        if rel:
            links[rel] = url
    return links


def fetch_json(url: str, token: str) -> tuple:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "github-clone.py")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))
        link_header = response.headers.get("Link", "")
        return data, link_header


def fetch_all_repos(
    api_base_url: str, token: str, username: str, per_page: int, affiliation: str
) -> list:
    repos = []

    if token:
        # affiliation controls which repos the authenticated account can see, e.g.
        # "owner" excludes repos you were only invited to as a collaborator/org member
        url = f"{api_base_url}/user/repos?per_page={per_page}&affiliation={affiliation}"
    elif username:
        # No token: only public repositories of this user are visible
        url = f"{api_base_url}/users/{username}/repos?per_page={per_page}"
    else:
        raise ValueError("Either 'token' or 'username' must be set in the config file.")

    while url:
        data, link_header = fetch_json(url, token)
        repos.extend(data)
        url = parse_link_header(link_header).get("next")

    return repos


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch all GitHub repositories' SSH clone URLs and save them to a text file."
    )
    parser.add_argument(
        "-e",
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help=f"Path to the .env parameter file (default: {DEFAULT_ENV_FILE}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=f"Output text file path (default: value from .env, or {DEFAULT_OUTPUT_FILE}).",
    )
    args = parser.parse_args()

    config = load_config(Path(args.env_file))

    token = str(config.get("GITHUB_TOKEN", "")).strip()
    username = str(config.get("GITHUB_USERNAME", "")).strip()
    api_base_url = str(config.get("GITHUB_API_BASE_URL", DEFAULT_API_BASE_URL)).rstrip("/")
    per_page = int(config.get("GITHUB_PER_PAGE", DEFAULT_PER_PAGE))
    affiliation = str(config.get("GITHUB_AFFILIATION", DEFAULT_AFFILIATION)).strip()
    output_file = args.output or config.get("GITHUB_OUTPUT_FILE", DEFAULT_OUTPUT_FILE)

    if not token and not username:
        print(
            f"Error: '{args.env_file}' must define GITHUB_TOKEN (required to list "
            "private repositories) or at least GITHUB_USERNAME (public repositories only).",
            file=sys.stderr,
        )
        return 2

    try:
        repos = fetch_all_repos(api_base_url, token, username, per_page, affiliation)
    except urllib.error.HTTPError as e:
        print(f"Error: GitHub API request failed: HTTP {e.code} {e.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Error: could not reach GitHub API: {e.reason}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    entries = []
    for repo in repos:
        ssh_url = repo.get("ssh_url")
        if not ssh_url:
            continue
        visibility = "private" if repo.get("private") else "public"
        entries.append((visibility, ssh_url))

    entries.sort(key=lambda entry: entry[1])

    # Pad the visibility label to the width of "private" so the SSH URLs line up
    label_width = len("private")
    lines = [f"{visibility:<{label_width}} {ssh_url}" for visibility, ssh_url in entries]

    output_path = Path(output_file)
    output_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    print(f"Fetched {len(lines)} repositories. Saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
