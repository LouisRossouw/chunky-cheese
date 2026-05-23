import time
import threading
import uvicorn
from fastapi import FastAPI
from routers import router
import led


def heartbeat_loop():
    while True:
        time.sleep(5)
        # Pulse dim white flash for 100ms, then off
        led.run([
            {"colors": [(0, 0, 0), (10, 10, 10), (0, 0, 0)], "duration": 0.1},
            {"colors": [(0, 0, 0), (0, 0, 0), (0, 0, 0)], "duration": 0.0}
        ])


class ServiceApi:
    def __init__(self):
        self.app = FastAPI()

        self._include_routers()

        # Start the background heartbeat thread
        self.heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def _include_routers(self):
        self.app.include_router(router)

    def run(self, host="0.0.0.0", port=4001):
        uvicorn.run(self.app, host=host, port=port)
