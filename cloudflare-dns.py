#!/usr/bin/env python3
"""
Create or update a single Cloudflare DNS record so it matches the given
content, using parameters read from a .env file (with CLI overrides).

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
DEFAULT_API_BASE_URL = "https://api.cloudflare.com/client/v4"
DEFAULT_RECORD_TYPE = "A"
DEFAULT_TTL = "1"
DEFAULT_PROXIED = "false"

ENV_KEYS = (
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_API_KEY",
    "CLOUDFLARE_API_EMAIL",
    "CLOUDFLARE_API_BASE_URL",
    "CLOUDFLARE_ZONE_ID",
    "CLOUDFLARE_ZONE_NAME",
    "CLOUDFLARE_RECORD_NAME",
    "CLOUDFLARE_RECORD_TYPE",
    "CLOUDFLARE_RECORD_CONTENT",
    "CLOUDFLARE_RECORD_TTL",
    "CLOUDFLARE_RECORD_PROXIED",
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


def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def build_auth_headers(token: str, api_key: str, email: str) -> dict:
    if token:
        return {"Authorization": f"Bearer {token}"}
    if api_key and email:
        return {"X-Auth-Key": api_key, "X-Auth-Email": email}
    raise ValueError(
        "Set CLOUDFLARE_API_TOKEN, or both CLOUDFLARE_API_KEY and CLOUDFLARE_API_EMAIL, in the config."
    )


def api_request(api_base_url: str, headers: dict, method: str, path: str, payload: dict = None) -> dict:
    url = f"{api_base_url}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None

    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", "cloudflare-dns.py")
    for key, value in headers.items():
        request.add_header(key, value)

    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")

    try:
        body = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Unexpected non-JSON response from Cloudflare API: {raw[:200]!r}") from e

    if not body.get("success", False):
        errors = "; ".join(err.get("message", str(err)) for err in body.get("errors", []))
        raise RuntimeError(errors or f"Cloudflare API request failed: {method} {path}")

    return body


def resolve_zone_id(api_base_url: str, headers: dict, zone_id: str, zone_name: str) -> str:
    if zone_id:
        return zone_id
    if not zone_name:
        raise ValueError("Set CLOUDFLARE_ZONE_ID or CLOUDFLARE_ZONE_NAME in the config.")

    body = api_request(api_base_url, headers, "GET", f"/zones?name={zone_name}")
    results = body.get("result", [])
    if not results:
        raise ValueError(f"No Cloudflare zone found for name: {zone_name}")
    return results[0]["id"]


def find_dns_record(api_base_url: str, headers: dict, zone_id: str, name: str, record_type: str):
    body = api_request(
        api_base_url,
        headers,
        "GET",
        f"/zones/{zone_id}/dns_records?type={record_type}&name={name}",
    )
    results = body.get("result", [])
    return results[0] if results else None


def upsert_dns_record(
    api_base_url: str,
    headers: dict,
    zone_id: str,
    name: str,
    record_type: str,
    content: str,
    ttl: int,
    proxied: bool,
) -> str:
    existing = find_dns_record(api_base_url, headers, zone_id, name, record_type)

    payload = {
        "type": record_type,
        "name": name,
        "content": content,
        "ttl": ttl,
        "proxied": proxied,
    }

    if existing is None:
        api_request(api_base_url, headers, "POST", f"/zones/{zone_id}/dns_records", payload)
        return "created"

    if (
        existing.get("content") == content
        and existing.get("ttl") == ttl
        and existing.get("proxied") == proxied
    ):
        return "unchanged"

    api_request(api_base_url, headers, "PUT", f"/zones/{zone_id}/dns_records/{existing['id']}", payload)
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create or update a Cloudflare DNS record so it matches the given content."
    )
    parser.add_argument(
        "-e",
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help=f"Path to the .env parameter file (default: {DEFAULT_ENV_FILE}).",
    )
    parser.add_argument("--zone-id", default=None, help="Cloudflare zone ID (overrides CLOUDFLARE_ZONE_ID).")
    parser.add_argument("--zone-name", default=None, help="Zone domain name, e.g. example.com (overrides CLOUDFLARE_ZONE_NAME).")
    parser.add_argument("--name", default=None, help="DNS record name, e.g. sub.example.com (overrides CLOUDFLARE_RECORD_NAME).")
    parser.add_argument("--type", default=None, help="DNS record type, e.g. A, AAAA, CNAME, TXT (overrides CLOUDFLARE_RECORD_TYPE).")
    parser.add_argument("--content", default=None, help="DNS record content/value (overrides CLOUDFLARE_RECORD_CONTENT).")
    parser.add_argument("--ttl", default=None, type=int, help="TTL in seconds, 1 means automatic (overrides CLOUDFLARE_RECORD_TTL).")

    proxied_group = parser.add_mutually_exclusive_group()
    proxied_group.add_argument("--proxied", dest="proxied", action="store_true", default=None, help="Enable the Cloudflare proxy for this record.")
    proxied_group.add_argument("--no-proxied", dest="proxied", action="store_false", help="Disable the Cloudflare proxy for this record.")

    args = parser.parse_args()

    config = load_config(Path(args.env_file))

    token = str(config.get("CLOUDFLARE_API_TOKEN", "")).strip()
    api_key = str(config.get("CLOUDFLARE_API_KEY", "")).strip()
    email = str(config.get("CLOUDFLARE_API_EMAIL", "")).strip()
    api_base_url = str(config.get("CLOUDFLARE_API_BASE_URL", DEFAULT_API_BASE_URL)).rstrip("/")

    zone_id = args.zone_id or str(config.get("CLOUDFLARE_ZONE_ID", "")).strip()
    zone_name = args.zone_name or str(config.get("CLOUDFLARE_ZONE_NAME", "")).strip()

    name = args.name or str(config.get("CLOUDFLARE_RECORD_NAME", "")).strip()
    record_type = (args.type or str(config.get("CLOUDFLARE_RECORD_TYPE", DEFAULT_RECORD_TYPE))).strip().upper()
    content = args.content or str(config.get("CLOUDFLARE_RECORD_CONTENT", "")).strip()
    ttl = args.ttl if args.ttl is not None else int(config.get("CLOUDFLARE_RECORD_TTL", DEFAULT_TTL))
    proxied = (
        args.proxied
        if args.proxied is not None
        else str_to_bool(config.get("CLOUDFLARE_RECORD_PROXIED", DEFAULT_PROXIED))
    )

    if not name or not content:
        print(
            f"Error: '{args.env_file}' must define CLOUDFLARE_RECORD_NAME and CLOUDFLARE_RECORD_CONTENT "
            "(or pass --name/--content).",
            file=sys.stderr,
        )
        return 2

    try:
        headers = build_auth_headers(token, api_key, email)
        resolved_zone_id = resolve_zone_id(api_base_url, headers, zone_id, zone_name)
        result = upsert_dns_record(api_base_url, headers, resolved_zone_id, name, record_type, content, ttl, proxied)
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Error: could not reach Cloudflare API: {e.reason}", file=sys.stderr)
        return 1

    print(f"DNS record {result}: {record_type} {name} -> {content} (ttl={ttl}, proxied={proxied})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
