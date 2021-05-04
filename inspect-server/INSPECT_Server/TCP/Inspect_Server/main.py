from Inspect_Server.settings import ADDR
from Inspect_Server.server import Server, Handler


def main():
    server = Server(ADDR, Handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
