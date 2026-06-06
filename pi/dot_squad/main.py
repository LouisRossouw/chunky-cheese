from core.config import Config
from api.service_api import ServiceApi

# TODO; Config should also define the host & port number

config = Config()
server = ServiceApi(config)
app = server.app

if __name__ == "__main__":
    server.run(host="127.0.0.1", port=4001)
