import uvicorn
from fastapi import FastAPI
from routers import router


class ServiceApi:
    def __init__(self):
        self.app = FastAPI()

        self._include_routers()

    def _include_routers(self):
        self.app.include_router(router)

    def run(self, host="0.0.0.0", port=4001):
        uvicorn.run(self.app, host=host, port=port)
