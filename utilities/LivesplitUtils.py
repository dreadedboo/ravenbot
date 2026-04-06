import socket

from utilities.CoreUtils import openfile, logger

LOGGER = logger("LivesplitUtils")
config = openfile("resources/livesplit_server_cfg.json")

HOST = config["host"]
PORT = config["port"]

def ping_livesplit_server():
    x = 0
    while x < 6:
        try:
            # Create socket and connect to LiveSplit Server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
            LOGGER.info("Connected to livesplit server")
            return True
        except ConnectionRefusedError:
            x += 1
    LOGGER.error("Failed to connect to Livesplit server")
    return False


def send_receive(command: str):
    try:
        # Create socket and connect to LiveSplit Server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((HOST, PORT))
            try:
                s.sendall(f"{command}\r\n".encode('utf-8'))
                data: str = s.recv(1024).decode('UTF-8')
            except TimeoutError:
                LOGGER.error("Livesplit server connection timed out")
                return False
            LOGGER.info(f"Command: {command} ran successfully. Received: {data[:-1]}")
        return data
    except ConnectionRefusedError:
        LOGGER.error("Failed to connect to Livesplit server")
        return False