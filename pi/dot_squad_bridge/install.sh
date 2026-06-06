#!/bin/bash

# Install script for Dot Squad Bridge extension
# This script ensures the extension is available at /opt/dot_squad_bridge

set -e

USER_NAME=${SUDO_USER:-$(whoami)}
INSTALL_DIR="/opt/dot_squad_bridge"

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

echo "Installing Dot Squad Bridge Extension..."

# Create install directory
echo "Creating directory $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR

# Copy extension files
echo "Copying extension files..."
sudo cp manifest.json $INSTALL_DIR/
sudo cp background.js $INSTALL_DIR/
sudo cp content.js $INSTALL_DIR/

# Set permissions
echo "Setting permissions..."
sudo chown -R $USER_NAME:$USER_NAME $INSTALL_DIR

echo "Dot Squad Bridge installation complete!"
