# Dot Squad: Pi LED Micro Service

<p align="center">
  <img src="https://github.com/user-attachments/assets/36e37c52-8302-42d5-ac3c-83b42f21e959" width="32%" />
  <img src="https://github.com/user-attachments/assets/1203f8ed-4b89-4186-8056-d13ef5c71cde" width="32%" />
  <img src="https://github.com/user-attachments/assets/a7f22471-5a03-4bbb-ac26-b748957aae02" width="32%" />
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

### Bridge Chrome extension

If you want a front end web app to communicate with the led hardware, it can be done using the bridge chrome extension - chunky-cheese/pi/dot_squad_bridge

The chrome extension needs to be installed on the browser of the device that has dot squad led hardware attached
You can now pass led patterns to the chrome extension and the extension forwards those requests to the Dot Squad service at localhost:4001.

```bash
window.postMessage(
  {
    type: "LED_TRIGGER",
    pattern: "low_kwh_alert", // this will trigger this animation pi\dot_squad\core\anims\low_kwh_alert.json
  },
  "*",
);
```

anim directories:

anims_overides directory:
Add custom animations to the pi\dot_squad\core\anims_overides directory, this allows you to overide the current anims, for example add heartbeat.json and it will overide the default heartbeat

anims directory:
Just a bunch of default anims

plugins:
Use chatgpt or an AI agent to generate animations as .py files, using loops etc
