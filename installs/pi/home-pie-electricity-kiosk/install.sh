#!/bin/bash

# Install Chromium
sudo apt update
sudo apt install -y chromium

# Create config directory
mkdir -p ~/.config/kiosk

# Copy files
cp start-kiosk.sh ~/start-kiosk.sh
cp .env ~/.config/kiosk/.env

# Make executable
chmod +x ~/start-kiosk.sh

# Add to autostart
mkdir -p ~/.config/lxsession/LXDE-pi

cat <<EOF > ~/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@~/start-kiosk.sh
EOF

echo "Kiosk setup complete!"