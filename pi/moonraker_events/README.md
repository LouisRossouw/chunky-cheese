# moonraker_events

A daemon that subscribes to [Moonraker](https://moonraker.readthedocs.io/) WebSocket events and drives addressable NeoPixel LED segments on an Ender 3D printer based on printer state.

## Features

- Reacts to printer events (heating, printing, errors, completion) and maps them to LED animations per segment
- REST API (FastAPI) for manual control and testing — supports switching between `auto` (Moonraker-driven) and `manual` mode
- Modular animation system — each LED segment can run an independent animation
- Runs as a `systemd` service at boot

## Project Structure

```
moonraker_events/
├── main.py           # Entry point; manages async loops
├── api.py            # FastAPI REST API
├── state.py          # Printer state model
├── manager.py        # Maps printer state → LED segment animations
├── renderer.py       # Writes animations to physical LEDs
├── animation.py      # Base animation class
├── animations/       # Individual animation implementations
├── segments.json     # LED segment configuration
├── moonraker.py      # Moonraker WebSocket client
├── requirements.txt
└── service/
    └── moonraker_events.service  # systemd unit file
```

## Installation

```bash
# Deploy to /opt and set up the service
sudo cp -r . /opt/moonraker_events
cd /opt/moonraker_events
python3 -m venv venv
venv/bin/pip install -r requirements.txt

sudo cp service/moonraker_events.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable moonraker_events
sudo systemctl start moonraker_events
```

## Running Manually

```bash
# Run with Moonraker connection
python main.py

# Run without Moonraker (API-only, useful for testing)
python main.py --no-moonraker --port 4001
```

## API

Docs available at `http://<pi-ip>:4001/docs` when the service is running.

Key endpoints:

- `GET /status` — current printer state and LED mode
- `POST /mode` — switch between `auto` / `manual`
- `POST /segment/{id}/animation` — manually set an animation on a segment

## Requirements

- Raspberry Pi with NeoPixel LED strip wired up
- Moonraker running on the same network
- Python 3.10+
