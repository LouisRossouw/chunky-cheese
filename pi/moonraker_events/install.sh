#!/bin/bash

set -e

SERVICE_NAME="moonraker_events"
INSTALL_DIR="/opt/moonraker_events"
USER_NAME=${SUDO_USER:-$(whoami)}

# Must run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "Installing Moonraker Events..."

# System dependencies
echo "Installing system packages..."
apt update
apt install -y python3 python3-venv python3-pip git

# Copy project
echo "Copying project to $INSTALL_DIR..."

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR"

chown -R root:root "$INSTALL_DIR"

cd "$INSTALL_DIR"

# Python venv
echo "Creating virtual environment..."

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

deactivate

# Install systemd service
echo "Installing systemd service..."

SERVICE_SRC="$INSTALL_DIR/service/moonraker_events.service"
SERVICE_DEST="/etc/systemd/system/moonraker_events.service"

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
echo ""
echo "✅ Moonraker Events installed successfully!"
echo ""
echo "Service status:"
systemctl status "$SERVICE_NAME" --no-pager
