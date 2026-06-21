
import websockets


class MoonrakerClient:
    def __init__(self):
        self.url = "ws://10.0.0.161:7125/websocket"

    async def connect(self):
        return await websockets.connect(self.url)
