import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()


class Token:
    def __init__(self) -> None:
        self.access_token: str
        self.token_type: str
        self.expires_in: int

    def get_token(self) -> None:
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


token = Token().get_token()
