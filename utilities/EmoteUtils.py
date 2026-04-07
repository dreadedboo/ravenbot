import requests

class SevenTVConnection:
    def __init__(self, token):
        self.data = {'code': token, 'platform': "twitch"}
        self.cr = requests.post(url="https://api.7tv.app/v4/auth/login/finish", data=self.data)
        print(self.cr.headers)