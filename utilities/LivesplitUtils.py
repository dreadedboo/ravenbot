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
        except ConnectionRefusedError:
            LOGGER.error("Failed to connect to Livesplit server")

    def get_string(self, command: str) -> bool | str:
        self.settimeout(5.0)
        try:
            self.sendall(f"{command}\r\n".encode('utf-8'))
            data: str = self.recv(1024).decode('UTF-8')
        except TimeoutError:
            LOGGER.error("Livesplit server connection timed out")
            return False
        LOGGER.info(f"Command: {command} ran successfully. Received: {data[:-1]}")
        return data[:-1]


    def get_time(self, command: str) -> bool | str:
        self.settimeout(5.0)
        try:
            self.sendall(f"{command}\r\n".encode('utf-8'))
            data: str = self.recv(1024).decode('UTF-8')
        except TimeoutError:
            LOGGER.error("Livesplit server connection timed out")
            return False
        LOGGER.info(f"Command: {command} ran successfully. Received: {data[:-9]}")
        return data[:-9]