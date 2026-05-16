#!/bin/bash

set -e

USER_NAME=${SUDO_USER:-$(whoami)}
SERVICE_NAME="motion-display"
INSTALL_DIR="/opt/motion-display-controller"

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

echo "Installing Motion Display Controller..."

echo "Installing config..."
sudo mkdir -p $INSTALL_DIR/config
sudo cp motion.conf $INSTALL_DIR/config/

# Install dependencies
echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-gpiozero

# Copy project files
echo "Copying files to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r . $INSTALL_DIR

# Set permissions
echo "Setting permissions..."
sudo chown -R $USER_NAME:$USER_NAME $INSTALL_DIR

# Install systemd service
echo "Installing systemd service for user $USER_NAME..."
# Create a temp service file with the correct user
cp service/$SERVICE_NAME.service /tmp/$SERVICE_NAME.service
sed -i "s/^User=.*/User=$USER_NAME/" /tmp/$SERVICE_NAME.service
sudo cp /tmp/$SERVICE_NAME.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service

# Start service
echo "Starting service..."
sudo systemctl restart $SERVICE_NAME.service

echo "Installation complete!"
echo "Status:"
sudo systemctl status $SERVICE_NAME.service --no-pager