#!/bin/bash

# Install script for Nav-Nav extension
# This script ensures the extension is available at /opt/nav-nav

set -e

USER_NAME=${SUDO_USER:-$(whoami)}
INSTALL_DIR="/opt/nav-nav"

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

echo "Installing Nav-Nav Extension..."

# Create install directory
echo "Creating directory $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR

# Copy extension files
echo "Copying extension files..."
sudo cp -r . $INSTALL_DIR/

# Set permissions
echo "Setting permissions..."
sudo chown -R $USER_NAME:$USER_NAME $INSTALL_DIR

echo "Nav-Nav installation complete!"
