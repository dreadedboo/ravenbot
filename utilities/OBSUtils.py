import obsws_python as obs
from obsws_python import ReqClient

from utilities.CoreUtils import logger, openfile

LOGGER = logger("OBSUtils")

config = openfile("resources/obs_cfg.json")

HOST = config["host"]
PORT = config["port"]
PASSWD = config["pass"]


class OBSConnection(ReqClient):
    def __init__(self):
        try:
            super().__init__(host=HOST, port=PORT, password=PASSWD, timeout=3)
        except ConnectionError:
            LOGGER.error("Failed to connect to OBS")

    def reconnect(self) -> bool:
        try:
            super().__init__(host=HOST, port=PORT, password=PASSWD, timeout=3)
            return True
        except ConnectionError:
            LOGGER.error("Failed to connect to OBS")
            return False
