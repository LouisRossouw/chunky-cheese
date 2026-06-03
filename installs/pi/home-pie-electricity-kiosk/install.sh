#!/bin/bash

# Master Install Script for Dynamic Kiosk Setup
# This script reads from installs.list and executes specified sub-installers.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}   Chunky Cheese - Dynamic Kiosk Installer          ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Ensure we are running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Error: Please run as root (use sudo).${NC}"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/installs.list"
# Repo root is 3 levels up from installs/pi/home-pie-electricity-kiosk/
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [ ! -f "$CONFIG_FILE" ]; then
  echo -e "${RED}Error: Configuration file $CONFIG_FILE not found.${NC}"
  exit 1
fi

echo -e "${BLUE}Reading installation list from: $CONFIG_FILE${NC}"
echo -e "${BLUE}Repository root: $REPO_ROOT${NC}"
echo ""

# Loop through each line in installs.list
while IFS= read -r install_path || [ -n "$install_path" ]; do
  # Skip comments and empty lines
  [[ "$install_path" =~ ^#.*$ ]] && continue
  [[ -z "$install_path" ]] && continue

  # Determine if path is absolute or relative
  if [[ "$install_path" = /* ]] || [[ "$install_path" =~ ^[a-zA-Z]:[/\] ]]; then
    FULL_PATH="$install_path"
  else
    FULL_PATH="$REPO_ROOT/$install_path"
  fi

  # Convert backslashes to forward slashes if needed (for Windows-style paths)
  FULL_PATH=$(echo "$FULL_PATH" | sed 's/\\/\//g')

  if [ -f "$FULL_PATH" ]; then
    INSTALL_DIR="$(dirname "$FULL_PATH")"
    INSTALL_SCRIPT="$(basename "$FULL_PATH")"

    echo -e "${GREEN}>>> Starting installation: $INSTALL_PATH${NC}"
    echo -e "${GREEN}>>> Path: $FULL_PATH${NC}"
    
    # Change into the directory of the install script
    pushd "$INSTALL_DIR" > /dev/null
    
    # Ensure script is executable
    chmod +x "$INSTALL_SCRIPT"
    
    # Execute the script
    # We use -E to preserve environment variables like SUDO_USER
    if sudo -E ./"$INSTALL_SCRIPT"; then
      echo -e "${GREEN}<<< Finished installation: $INSTALL_PATH${NC}"
    else
      echo -e "${RED}<<< Installation FAILED: $INSTALL_PATH${NC}"
      popd > /dev/null
      exit 1
    fi
    
    popd > /dev/null
    echo ""
  else
    echo -e "${RED}Warning: Script not found at $FULL_PATH${NC}"
  fi

done < "$CONFIG_FILE"

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}   All installations completed successfully!        ${NC}"
echo -e "${BLUE}====================================================${NC}"