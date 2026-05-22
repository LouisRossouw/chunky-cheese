#!/bin/bash

set -e

SERVICE_NAME="dot-squad"
INSTALL_DIR="/opt/dot-squad"
SERVICE_FILE="${SERVICE_NAME}.service"

USER_NAME=${SUDO_USER:-$(whoami)}

# Must run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "Installing Dot Squad..."

# System dependencies
echo "Installing system packages..."
apt update
apt install -y python3 python3-venv python3-pip git

# Copy project to /opt
echo "Setting up install directory..."

mkdir -p "$INSTALL_DIR"

# If running from repo directory
cp -r . "$INSTALL_DIR"

chown -R $USER_NAME:$USER_NAME "$INSTALL_DIR"

cd "$INSTALL_DIR"

# Create virtual environment
echo "Creating virtual environment..."

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Install systemd service
echo "Installing systemd service..."

SERVICE_PATH="/etc/systemd/system/$SERVICE_FILE"

cat <<EOF > $SERVICE_PATH
[Unit]
Description=Dot Squad LED API Server
After=network.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$INSTALL_DIR

ExecStart=$INSTALL_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 4001

Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Enable service
echo "Reloading systemd..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl restart $SERVICE_NAME

# Done
echo "Dot Squad installed successfully!"
echo "Service status:"
systemctl status $SERVICE_NAME --no-pager

# Test
curl localhost:4001/run-led/notify_01