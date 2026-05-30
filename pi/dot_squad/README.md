# Dot Squad: Pi LED Micro Service

<p align="center">
  <img src="https://github.com/user-attachments/assets/5b3952eb-a1cf-4974-85d7-5a1e92353f3d" width="45%" />
  <img src="https://github.com/user-attachments/assets/1203f8ed-4b89-4186-8056-d13ef5c71cde" width="45%" />
</p>

Local running HTTP microservice for controlling the Dot Squad LED display (custom) on a Raspberry Pi.

## (Production) Installation

```bash
git clone https://github.com/LouisRossouw/chunky-cheese.git
cd chunky-cheese/pi/dot_squad
chmod +x install.sh
sudo ./install.sh
```

## Addressable LED Strip

- WS2812B
- 3 LEDs

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
