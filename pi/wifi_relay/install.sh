#!/bin/bash

set -e

SERVICE_NAME="wifi-relay"
INSTALL_DIR="/opt/wifi-relay"
USER_NAME=${SUDO_USER:-$(whoami)}

# Must run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "Installing WiFi Relay..."

# System dependencies
echo "Installing system packages..."
apt update
apt install -y python3 python3-venv python3-pip network-manager

# Copy project
echo "Copying project to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR"
chown -R $USER_NAME:$USER_NAME "$INSTALL_DIR"

cd "$INSTALL_DIR"

# Python venv
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Install systemd service
echo "Installing systemd service..."
SERVICE_SRC="$INSTALL_DIR/service/wifi-relay.service"
SERVICE_DEST="/etc/systemd/system/wifi-relay.service"

if [ ! -f "$SERVICE_SRC" ]; then
  echo "❌ Service file not found at $SERVICE_SRC"
  exit 1
fi

cp "$SERVICE_SRC" "$SERVICE_DEST"
chmod 644 "$SERVICE_DEST"

# Enable + start service
echo "Reloading systemd..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

# Done
echo "✅ WiFi Relay installed successfully!"
echo ""
echo "Service status:"
systemctl status "$SERVICE_NAME" --no-pager

# Test
echo ""
echo "Testing API..."
sleep 3
curl -s http://localhost:4005/health > /dev/null && echo "✅ API is running" || echo "⚠️ API not responding yet"
