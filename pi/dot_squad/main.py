from core.config import Config
from api.api import ServiceApi

# TODO; Config should also define the host & port number

config = Config()
server = ServiceApi(config)
app = server.app

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4001)
