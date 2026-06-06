# Dot Squad Bridge - Chrome Extension

Chrome extension bridge that triggers local [Dot Squad](file:///d:/work/projects/dev/projects/chunky-cheese/pi/dot_squad) LED patterns from the [Kiosk Dashboard](file:///d:/work/projects/dev/projects/kiosk/src/components/KioskDashboard.tsx).

The purpose of this bridge is to keep requests local; web apps communicate with the extension, and the extension forwards those requests to the Dot Squad service at localhost:4001.

## Installation

\*This needs to be installed on the server running the kiosk.

### Automated (Recommended)

Run the install script to make the extension available at `/opt/dot_squad_bridge`:

```bash
sudo ./install.sh
```

### Manual

1. Open `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select this folder

### How to use

After the install, you can now pass led patterns to the chrome extension from any front end web app

```bash
window.postMessage(
  {
    type: "LED_TRIGGER",
    pattern: "low_kwh_alert", // this will trigger this animation pi\dot_squad\core\anims\low_kwh_alert.json
  },
  "*",
);
```
