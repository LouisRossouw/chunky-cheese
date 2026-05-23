import time
import uvicorn
import threading
from fastapi import FastAPI

from led_map import led_animations
from routers import router
import led


def heartbeat_loop():
    while True:
        time.sleep(2)
        led.run(led_animations.get('heartbeat'))


class ServiceApi:
    def __init__(self):
        self.app = FastAPI()

        self._include_routers()

        # Start the background heartbeat thread
        self.heartbeat_thread = threading.Thread(
            target=heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def _include_routers(self):
        self.app.include_router(router)

    def run(self, host="0.0.0.0", port=4001):
        uvicorn.run(self.app, host=host, port=port)
