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
        except ConnectionRefusedError or ConnectionAbortedError:
            LOGGER.error("Failed to connect to Livesplit server")

    def get_string(self, command: str) -> str:
        data = ""
        self.settimeout(5.0)
        try:
            self.sendall(f"{command}\r\n".encode('utf-8'))
            try:
                data: str = self.recv(1024).decode('UTF-8')
                LOGGER.info(f"Command: {command} ran successfully. Received: {data[:-1]}")
                return data[:-1]
            except ConnectionAbortedError:
                LOGGER.error("Lost connection to LiveSplit")
        except TimeoutError:
            LOGGER.error("Livesplit server connection timed out")
        return data