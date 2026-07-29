# wifi_relay

A tiny FastAPI service that runs on the Raspberry Pi and exposes an HTTP endpoint to trigger a WiFi reconnect. Designed to be called from the `nav_nav` browser extension.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns `{"status": "ok"}` |
| `POST` | `/wifi/reconnect` | Toggles WiFi radio off then on via `nmcli` |

## Install

```bash
sudo ./install.sh
```

Copies to `/opt/wifi-relay`, sets up a Python venv, and installs a systemd service on **port 4005**.

## Requirements

- Raspberry Pi OS with NetworkManager (`nmcli`)
- Python 3

## Service management

```bash
sudo systemctl status wifi-relay
sudo systemctl restart wifi-relay
sudo journalctl -u wifi-relay -f
```

## nav_nav integration

The `nav_nav` extension's `config.json` already has a "Reconnect WiFi" script button pre-configured pointing at `http://localhost:4005/wifi/reconnect`. Once the service is running, the button will appear in the nav menu. Click it to trigger a reconnect.
