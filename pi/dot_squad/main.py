from api import ServiceApi

server = ServiceApi()
app = server.app

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4001)
