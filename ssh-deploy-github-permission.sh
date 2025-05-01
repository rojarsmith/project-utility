#!/bin/bash
set -e

# === CONFIG SECTION ===
echo "$1"
SUDO_PASS="$1"
GITHUB_USER="$2"
GITHUB_REPO="$3"
DEPLOY_KEY_TITLE="$4"
GITHUB_TOKEN="$5"
# KEY_FILE="$6" # Infinite loop
# SSH_CONFIG_FILE="$7"
KEY_FILE=/root/.ssh/id_rsa
SSH_CONFIG_FILE=/root/.ssh/config

echo "SUDO_PASS=$SUDO_PASS"

# === GENERATE SSH KEY IF NOT EXIST ===
if [ ! -f "$KEY_FILE" ]; then
    echo "Generating new SSH key..."
    ssh-keygen -t rsa -b 4096 -C "$USER@$(hostname)" -f "$KEY_FILE" -N ""
else
    echo "SSH key already exists at $KEY_FILE"
fi

# === ADD GITHUB TO KNOWN HOSTS ===
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null

# === READ PUBLIC KEY ===
PUB_KEY=$(cat "${KEY_FILE}.pub")

# === CALL GITHUB API TO ADD DEPLOY KEY ===
echo "Adding deploy key to GitHub repo..."
curl -s -X POST https://api.github.com/repos/$GITHUB_USER/$GITHUB_REPO/keys \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d @- <<EOF
{
  "title": "$DEPLOY_KEY_TITLE",
  "key": "$PUB_KEY",
  "read_only": false
}
EOF

# === WRITE SSH CONFIG ===
if ! grep -q "Host github.com" "$SSH_CONFIG_FILE" 2>/dev/null; then
  echo "Updating ~/.ssh/config..."
  cat >> "$SSH_CONFIG_FILE" <<EOF

Host $DEPLOY_KEY_TITLE-github.com
  HostName github.com
  User git
  IdentityFile $KEY_FILE
  IdentitiesOnly yes
EOF
  chmod 600 "$SSH_CONFIG_FILE"
else
  echo "~/.ssh/config already contains github.com section"
fi
