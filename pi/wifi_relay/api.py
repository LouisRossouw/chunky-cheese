import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WiFi Relay", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")


@app.get("/")
def index():
    return FileResponse(INDEX_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/wifi/reconnect")
def wifi_reconnect():
    """
    Toggle WiFi radio off then on via nmcli to force a reconnect.
    Requires NetworkManager (nmcli) which is standard on Raspberry Pi OS.
    """
    commands = [
        ["nmcli", "radio", "wifi", "off"],
        ["sleep", "2"],
        ["nmcli", "radio", "wifi", "on"],
    ]

    for cmd in commands:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0 and cmd[0] != "sleep":
                return {
                    "success": False,
                    "message": f"Command {' '.join(cmd)} failed: {result.stderr.strip()}",
                }
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Command not found: {cmd[0]}. Is nmcli installed?",
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": f"Command timed out: {' '.join(cmd)}",
            }

    return {"success": True, "message": "WiFi reconnect triggered successfully."}
