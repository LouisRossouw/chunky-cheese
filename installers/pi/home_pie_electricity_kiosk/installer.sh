#!/bin/bash
set -e
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root (use sudo)."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

MAIN_INSTALLER="$REPO_ROOT/installers/installer.sh"
CONFIG_FILE="$SCRIPT_DIR/installs.list"

bash "$MAIN_INSTALLER" --config "$CONFIG_FILE" "$@"