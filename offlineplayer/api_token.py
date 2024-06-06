import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()


class Token:
    def __init__(self) -> None:
        self.token: str = None
        self.access_token: str = None
        self.token_type: str = None
        self.expires_in: int = None

    @property
    def token(self) -> str:
        token = self.get_local_token()
        if not token:
            token = self.get_new_token()

        return token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value

    def get_local_token(self) -> str:
        if not os.path.exists("./token.json"):
            return None
        with open("token.json", "r") as jsonf:
            local_token: dict = json.load(jsonf)
            if local_token["timestamp"] + local_token["expires_in"] < time.time():
                return None
            return local_token["access_token"]

    def get_new_token(self) -> str:
        url: str = "https://accounts.spotify.com/api/token"
        headers: dict = {"Content-Type": "application/x-www-form-urlencoded"}
        data: dict = {
            "grant_type": "client_credentials",
            "client_id": os.environ["CLIENT_ID"],
            "client_secret": os.environ["CLIENT_SECRET"],
        }
        response: requests.Response = requests.post(
            url=url,
            headers=headers,
            data=data,
        )

        token_json: dict = response.json()
        token_json["timestamp"] = time.time()

        with open("token.json", "w+") as jsonf:
            json.dump(token_json, jsonf)

        return token_json["access_token"]


TOKEN = Token()
