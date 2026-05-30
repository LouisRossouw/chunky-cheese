from fastapi import FastAPI
import threading
import uvicorn

from api.routers import router
from core.dot_squad import DotSquad


class ServiceApi:
    def __init__(self, config):
        self.app = FastAPI()
        self.DS = DotSquad(config)

        self.app.state.config = config
        self.app.state.ds = self.DS

        # Start the background heartbeat thread
        self.heartbeat_thread = threading.Thread(target=self.DS.heartbeat_loop, daemon=True)  # nopep8
        self.heartbeat_thread.start()

        self._include_routers()

    def _include_routers(self):
        self.app.include_router(router)

    def run(self, host="0.0.0.0", port=4001):
        uvicorn.run(self.app, host=host, port=port)
