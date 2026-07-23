# Project Utility

## Git

### git-clone-alot.bat

Batch clone all GIT repositories in git-clone-alot.txt to the upper directory.

### git-pull-alot.bat

Search and batch pull all GIT projects on upper-level directory.

### project-list.bat

List the directory names of all GIT projects in the previous level

### github-repository.py

Fetch all GitHub repositories (public and private) for the authenticated user via
the GitHub REST API, and save their SSH clone URLs to `github-repository.txt`
(git-ignored). Each line starts with a visibility label padded to align with
`private`, followed by the SSH clone URL, e.g.:

```
private git@github.com:rojarsmith/ai-lab.git
public  git@github.com:rojarsmith/zen-menu.git
```

Setup:

1. Copy `.env.example` to `.env` (git-ignored, since it holds your token).
2. Fill in `GITHUB_TOKEN` with a GitHub Personal Access Token that has `repo`
   scope (required to list private repositories). If you only need public
   repositories, set `GITHUB_USERNAME` instead and leave `GITHUB_TOKEN` empty.
3. Run:

```bash
python3 github-repository.py
```

`.env` parameters:

- `GITHUB_TOKEN` — Personal Access Token with `repo` scope (enables private repos)
- `GITHUB_USERNAME` — used only when `GITHUB_TOKEN` is empty (public repos only)
- `GITHUB_API_BASE_URL` — default `https://api.github.com` (e.g. for GitHub Enterprise)
- `GITHUB_OUTPUT_FILE` — default `github-repository.txt`
- `GITHUB_PER_PAGE` — default `100`
- `GITHUB_AFFILIATION` — default `owner`. Controls which repos the token's
  account can see (passed straight to GitHub's `affiliation` API parameter):
  - `owner` — only repos owned by this account (excludes repos you were only
    invited to as a collaborator, and repos of organizations you belong to)
  - `collaborator` — repos you were added to as a collaborator
  - `organization_member` — repos of organizations you are a member of
  - comma-combine multiple values, e.g. `owner,organization_member`

  The default of `owner` avoids picking up other people's repos that invited
  your account as a collaborator (e.g. a repo like
  `git@github.com:someone-else/some-project.git` showing up just because you
  were added to it).

Real OS environment variables of the same name (handy in CI) always take
precedence over the `.env` file.

Optional flags:

- `-e, --env-file <path>` — use an alternate `.env` file (default: `.env`)
- `-o, --output <path>` — override the output file path (default: `github-repository.txt`, or the value from `.env`)

This tool only uses the Python standard library (`urllib`, plus a tiny
built-in `.env` parser), so no extra package installation is needed.

### github-clone.py

Reads `github-repository.txt` (produced by `github-repository.py`) and, for
every listed repository whose folder is missing from the parent directory,
runs `git clone` to fetch it there. Repositories that already have a local
folder are left untouched, so it's safe to run repeatedly.

Run:

```bash
python3 github-clone.py
```

Preview what would be cloned without actually cloning:

```bash
python3 github-clone.py --dry-run
```

`.env` parameters:

- `GITHUB_REPOSITORY_LIST_FILE` — default `github-repository.txt`
- `GITHUB_CLONE_TARGET_DIR` — default `..` (the parent directory, matching
  where `git-clone-alot.bat` clones repos to)

Optional flags:

- `-e, --env-file <path>` — use an alternate `.env` file (default: `.env`)
- `-i, --input <path>` — override the repository list file path
- `-d, --dir <path>` — override the directory to clone into
- `--dry-run` — list repositories that would be cloned, without cloning them

This tool uses only the Python standard library plus the system `git`
executable — no third-party package is installed. SSH clone URLs
(`git@github.com:...`) rely on your own SSH key already being set up with
GitHub; no token is needed by this script.

### github-pull.py

Reads `github-repository.txt` (produced by `github-repository.py`) and, for
every listed repository that already has a local folder in the parent
directory, runs `git pull` there. Repositories with no local folder are
skipped (use `github-clone.py` to fetch them first). Writes a plain-text
report to `github-pull.txt` (git-ignored), including the reason for any
failed pull — e.g. local file modifications or merge conflicts.

Run:

```bash
python3 github-pull.py
```

Example report:

```
GitHub Pull Report
Generated: 2026-07-18T14:57:05
Source list: github-repository.txt (4 entries)
Target directory: ..

[OK]             ok-repo       Fast-forward | file.txt | 1 file changed, 1 insertion(+)
[FAILED]         mismatch-repo error: Your local changes to the following files would be overwritten by merge: | shared.txt | Please commit your changes or stash them before you merge.
[NOT_A_GIT_REPO] not-a-git     folder exists but is not a git repository
[MISSING]        missing-repo  no local folder, nothing to pull

Summary: 1 FAILED, 1 MISSING, 1 NOT_A_GIT_REPO, 1 OK
```

`.env` parameters:

- `GITHUB_REPOSITORY_LIST_FILE` — default `github-repository.txt`
- `GITHUB_PULL_TARGET_DIR` — default `..` (the parent directory, matching
  where `git-clone-alot.bat` clones repos to)
- `GITHUB_PULL_REPORT_FILE` — default `github-pull.txt`

Optional flags:

- `-e, --env-file <path>` — use an alternate `.env` file (default: `.env`)
- `-i, --input <path>` — override the repository list file path
- `-d, --dir <path>` — override the directory containing the local repo folders
- `-o, --output <path>` — override the report output path

This tool uses only the Python standard library plus the system `git`
executable — no third-party package is installed. The exit code is non-zero
if any repository failed to pull, so it can be used as a CI gate.

### github-integrity.py

Cross-checks `github-repository.txt` (produced by `github-repository.py`)
against the local folders in the parent directory, and writes a plain-text
report to `github-integrity.txt` (git-ignored) so you can see what's missing
or extra at a glance. For every listed repo it checks:

- the folder exists next to this project (one level up),
- it is actually a git repository (`.git` is present),
- its `origin` remote matches the expected GitHub repo.

It also scans the parent directory for local git repos that aren't in the
list at all (`EXTRA`), e.g. repos that were deleted/renamed on GitHub or
filtered out by `GITHUB_AFFILIATION`.

Run:

```bash
python3 github-integrity.py
```

Example report:

```
GitHub Clone Integrity Report
Generated: 2026-07-18T01:15:56
Source list: github-repository.txt (4 entries)
Scanned directory: ..

[OK]              ai-lab        git@github.com:rojarsmith/ai-lab.git
[MISSING]         code-quiz     no local folder
[NOT_A_GIT_REPO]  quantcat      folder exists but is not a git repository
[REMOTE_MISMATCH] zen-menu      local remote is git@github.com:someone-else/zen-menu.git

Extra local git repositories not listed in the repository list:
[EXTRA] old-project remote: git@github.com:rojarsmith/old-project.git

Summary: 1 MISSING, 1 NOT_A_GIT_REPO, 1 OK, 1 REMOTE_MISMATCH, 1 EXTRA
```

`.env` parameters:

- `GITHUB_REPOSITORY_LIST_FILE` — default `github-repository.txt`
- `GITHUB_INTEGRITY_REPORT_FILE` — default `github-integrity.txt`
- `GITHUB_INTEGRITY_PARENT_DIR` — default `..` (the parent directory, matching
  where `git-clone-alot.bat` clones repos to)

Optional flags:

- `-e, --env-file <path>` — use an alternate `.env` file (default: `.env`)
- `-i, --input <path>` — override the repository list file path
- `-d, --dir <path>` — override the directory to scan
- `-o, --output <path>` — override the report output path

This tool uses only the Python standard library plus the system `git`
executable (already required to clone these repos in the first place) —
no third-party package is installed.

## Cloudflare

### cloudflare-dns.py

Creates or updates a single Cloudflare DNS record so it matches a given
value, using the Cloudflare API. If the record doesn't exist it is created;
if it exists with different content/TTL/proxy settings it is updated; if it
already matches, nothing is changed.

Setup:

1. Copy `.env.example` to `.env` (git-ignored, since it holds your credentials).
2. Fill in `CLOUDFLARE_API_TOKEN` (a scoped API Token with `Zone:DNS:Edit`
   permission on the target zone — create one at
   https://dash.cloudflare.com/profile/api-tokens). Alternatively, set the
   legacy `CLOUDFLARE_API_KEY` + `CLOUDFLARE_API_EMAIL` pair.
3. Set `CLOUDFLARE_ZONE_NAME` (or `CLOUDFLARE_ZONE_ID` if you already know it),
   `CLOUDFLARE_RECORD_NAME`, `CLOUDFLARE_RECORD_TYPE`, and
   `CLOUDFLARE_RECORD_CONTENT`.
4. Run:

```bash
python cloudflare-dns.py
```

`.env` parameters:

- `CLOUDFLARE_API_TOKEN` — preferred auth method, a scoped API Token
- `CLOUDFLARE_API_KEY` / `CLOUDFLARE_API_EMAIL` — legacy Global API Key auth,
  used only when `CLOUDFLARE_API_TOKEN` is empty
- `CLOUDFLARE_API_BASE_URL` — default `https://api.cloudflare.com/client/v4`
- `CLOUDFLARE_ZONE_ID` — the zone to operate on; takes priority over `CLOUDFLARE_ZONE_NAME`
- `CLOUDFLARE_ZONE_NAME` — used to look up the zone ID when `CLOUDFLARE_ZONE_ID` is empty
- `CLOUDFLARE_RECORD_NAME` — the DNS record to create/update, e.g. `sub.example.com`
- `CLOUDFLARE_RECORD_TYPE` — default `A`
- `CLOUDFLARE_RECORD_CONTENT` — the value the record should be set to, e.g. an IP address
- `CLOUDFLARE_RECORD_TTL` — default `1` (Cloudflare's "automatic" TTL)
- `CLOUDFLARE_RECORD_PROXIED` — default `false`

Real OS environment variables of the same name (handy in CI) always take
precedence over the `.env` file.

Optional flags (each overrides the matching `.env` value for a single run):

- `-e, --env-file <path>` — use an alternate `.env` file (default: `.env`)
- `--zone-id <id>` / `--zone-name <name>`
- `--name <record>` / `--type <A|AAAA|CNAME|...>` / `--content <value>` / `--ttl <seconds>`
- `--proxied` / `--no-proxied`

This is handy for simple dynamic-DNS style updates, e.g.:

```bash
python3 cloudflare-dns.py --content "$(curl -s https://api.ipify.org)"
```

This tool only uses the Python standard library (`urllib`), so no extra
package installation is needed.

## Frontend Debug

chrome --incognito --headless --remote-debugging-port=9222
C:/Users/dev/Desktop/GoogleChromePortable64/GoogleChromePortable.exe --private-window

## VMware

Create a linked ubuntu vm for test.

```shell
vmws-lab-ubu.bat templateDir "D:\vmubu2404sv" outputRoot "D:" vmName "vmubu2404sv1"

ping -4 vmubu2404sv1
```

Preinstall

```bash
sudo apt install -y open-vm-tools
sudo systemctl enable --now open-vm-tools
# Ping host name
sudo apt install avahi-daemon -y
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

## Prompt Guidelines for AI-Generated Dev Tools

This repo is full of small scripts generated with AI assistance. To keep them
consistent and low-maintenance, reuse the following requirements whenever you
ask an AI to write a new tool for this project:

- **Cross-platform first** — must run unmodified on Windows, macOS, and Linux
  (use `pathlib` instead of raw string paths, avoid shelling out to OS-specific
  commands, guard any unavoidable OS branch with `os.name`/`sys.platform`).
- **Minimize external dependencies** — prefer the standard library. If a
  third-party package is unavoidable, auto-bootstrap an isolated `.venv`
  (see `nginx-formatter.py` / `png-to-favicon.py`) instead of requiring a
  global `pip install`.
- **Externalize configuration** — secrets and tunable parameters (tokens,
  URLs, usernames, output paths) must be read from a config file (e.g. `.env`
  or `*.config.json`), never hardcoded or hand-typed on the command line.
  Commit an example template (`.env.example`, `*.example.json`, ...), and add
  the real config file to `.gitignore`.
- **Single responsibility per tool** — one script does exactly one job.
  Split unrelated features into separate tools instead of piling
  subcommands/flags onto one script.
- **Self-documenting CLI** — use `argparse` (or equivalent) so `--help`
  always works, with sensible defaults and meaningful exit codes.
- **English-only code** — all code, comments, and CLI text are written in
  English regardless of the language used to request the tool.
- **Git-ignore generated output** — any user-specific or regenerable output
  file belongs in `.gitignore`, not in version control.

A reusable prompt template following these rules:

```text
Write a <language> command-line tool named "<tool-name>" that <one clear task>.

Requirements:
- Cross-platform: must run unmodified on Windows, macOS, and Linux.
- Minimize external dependencies: prefer the standard library; only add a
  third-party package if there is no reasonable stdlib alternative, and
  bootstrap it via an auto-created virtual environment rather than requiring
  a global install.
- Externalize configuration: any secret or tunable parameter (API tokens,
  URLs, usernames, output paths) must be read from a config file (e.g. .env
  or a JSON/INI config), not hardcoded or passed as a plaintext CLI argument.
  Provide a committed example template (.env.example, *.example.json, ...)
  and add the real config file to .gitignore.
- Single responsibility: the tool should do exactly one job. Do not bundle
  multiple unrelated features behind subcommands.
- Provide --help via argparse with sensible defaults and meaningful exit codes.
- Write all code, comments, and CLI text in English.
- Any generated/user-specific output file should be listed in .gitignore.
```

