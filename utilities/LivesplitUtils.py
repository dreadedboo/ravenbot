# functions to interact with the LiveSplit server

from socket import socket, AF_INET, SOCK_STREAM

from utilities.CoreUtils import openfile, logger

LOGGER = logger("LivesplitUtils")
config = openfile("resources/livesplit_server_cfg.json")

HOST = config["host"]
PORT = config["port"]


class LivesplitConnection(socket):

    def __init__(self):
        super().__init__(AF_INET, SOCK_STREAM)
        try:
            self.connect((HOST, PORT))
            LOGGER.info("Connected to LiveSplit Server")
        except ConnectionError:
            LOGGER.error("Failed to connect to Livesplit server")

    def get_string(self, command: str) -> str:
        data = ""
        try:
            self.settimeout(5.0)
            self.sendall(f"{command}\r\n".encode('utf-8'))
            try:
                data: str = self.recv(1024).decode('UTF-8')
                LOGGER.info(f"Command: {command} ran successfully. Received: {data[:-1]}")
                return data[:-1]
            except ConnectionError or TimeoutError:
                LOGGER.error("Lost connection to LiveSplit")
        except OSError:
            self.close()
            self.__init__()
        return data
