# Dot Squad: Pi LED Micro Service

Local running HTTP microservice for controlling the Dot Squad LED display on a Raspberry Pi.

## (Production) Installation

```bash
git clone https://github.com/LouisRossouw/chunky-cheese.git
cd chunky-cheese/pi/dot_squad
chmod +x install.sh
sudo ./install.sh
```

## Wiring (Default)

| Dot Squad | Raspberry Pi |
| --------- | ------------ |
| VCC       | 3.3V         |
| GND       | GND          |
| DATA      | GPIO 18      |

## Optional (Development) setup

```bash
cd /opt/dot-squad
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo ./venv/bin/python main.py
```

## Usage

```bash
curl -X POST http://localhost:4001/run/notify_01
curl -X POST http://localhost:4001/run/boot

# Pass custom animations
curl -X POST http://localhost:4001/run-sequence -d '{
    "name": "notify_01",
    "loop": false,
    "frames": [
        {
            "colors": [
                [255, 0, 0],
                [0, 255, 0],
                [0, 0, 255]
            ],
            "duration": 0.5
        }
    ]
}'
```

or add it into other projects to call the led display.
