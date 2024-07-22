import os
import requests
import logging

from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("reccy")


class PlayerAPI:
    def __init__(self) -> None:
        self.url: str = "http://192.168.1.102:8085/"
        self.user_id: str = os.environ["USER_ID"]
        self.api_key: str = os.environ["API_KEY"]

    def get_api(self, endpoint: str, params: dict = {}, headers: dict = {}) -> dict:
        headers["X-Emby-Token"] = self.api_key

        response: requests.Response = requests.get(
            url=self.url + endpoint, params=params, headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f"API Status Code: {response.status_code}. Please check the issue."
            )
            return None

        return response.json()

    def get_now_playing(self) -> dict: ...


PLAYERAPI = PlayerAPI()
