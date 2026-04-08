# functions and classes to interact with emotes from various platforms

import requests

# class SevenTVConnection:
#     def __init__(self, token):
#         self.data = requests.get(url="https://7tv.io/v4/auth/login?platform=twitch")
#         print(self.data.headers)
#         self.user = requests.post(url="https://7tv.io/v4/auth/login/finish", json={"code": token, "platform": "twitch"})
#         print(self.user.text)