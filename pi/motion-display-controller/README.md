# Pi Motion Display Controller

Auto switch an IPS DSI display on, dim, and off based on motion detection.

Currently using it for Raspberry Pi 3B + with a HC-SR501 PIR sensor and an ISP DSI Display.

## Quick Install

1. Clone or copy this folder to your Raspberry Pi.
2. Run the installer:
   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```

## Management

- **Check Status**: `sudo systemctl status motion-display.service`
- **View Logs**: `sudo journalctl -u motion-display.service -f`
- **Config**: Edit `/opt/motion-display-controller/config/motion.conf`

## Wiring (Default)

| HC-SR501 Pin | Raspberry Pi |
| ------------ | ------------ |
| VCC          | 5V           |
| GND          | GND          |
| OUT          | GPIO 4       |


---


### OR Run directly (Development)

- (Just change the path to the config file in the python script.)

```bash
sudo python3 motion_display.py
```
