import requests

from utilities.CoreUtils import openfile

config = openfile("resources/src_config.json")

user = config["user"]

def send_get(d: dict):
    return requests.get(url=f"https://www.speedrun.com/api/v1/{d["url"]}")

def get_pb(game, username, category: str = None):
    data = send_get({
        "url": f"users/{username}/personal-bests?game=pm64&embed=game,category"
    }).json()
    print(dict(data))