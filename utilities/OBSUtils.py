import obsws_python as obs
from utilities.CoreUtils import logger, openfile

LOGGER = logger("OBSUtils")

config = openfile("resources/obs_cfg.json")

HOST = config["host"]
PORT = config["port"]
PASSWD = config["pass"]


def connect_to_obs():
    try:
        return obs.ReqClient(host=HOST, port=PORT, password=PASSWD, timeout=3)
    except ConnectionRefusedError:
        LOGGER.error("Failed to connect to OBS")
        return False
