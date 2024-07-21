import os
import random
import string
import hashlib
import requests
import xmltodict
import json
import logging
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("reccy")

NOW_PLAYING: str = "getNowPlaying"
GET_SONG: str = "getSong"
START_SCAN: str = "startScan"


class Subsonic:
    def __init__(self) -> None:
        self.url: str = (
            "http://192.168.1.102:8081/rest/"  # TODO: change the URL to container name
        )

    def is_playing(self) -> bool:
        now_playing: dict = self.get_api(NOW_PLAYING, "")
        if not now_playing["subsonic-response"]["nowPlaying"]:
            return False
        return True

    def get_song_info(self) -> dict:
        now_playing: dict = self.get_api(NOW_PLAYING, "")

        if not now_playing["subsonic-response"]["nowPlaying"]:
            return None

        with open("now_playing.json", "w") as jsonf:
            json.dump(now_playing, jsonf, indent=4)

        song_id: dict = now_playing["subsonic-response"]["nowPlaying"]["entry"]["@id"]
        song_info: dict = self.get_api(GET_SONG, song_id)
        return song_info

    def get_api(self, endpoint: str, song_id: str = "") -> dict:
        salt: str = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
        salted_pass: str = os.environ["SUBSONIC_PASS"] + salt
        hash_pass: str = hashlib.md5(salted_pass.encode()).hexdigest()

        params: dict = {
            "u": os.environ["SUBSONIC_USER"],
            "t": hash_pass,
            "s": salt,
            "v": os.environ["SUBSONIC_VERSION"],
            "c": os.environ["SUBSONIC_APP"],
        }

        if song_id != "":
            params["id"] = song_id

        response: requests.Response = requests.get(
            url=self.url + endpoint, params=params
        )

        data: dict = xmltodict.parse(response.text)
        return data

    def start_scan(self) -> None:
        self.get_api(START_SCAN)


SUBSONIC = Subsonic()
