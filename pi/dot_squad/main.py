from api import ServiceApi

server = ServiceApi()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4001)
