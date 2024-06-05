import os
import random
import string
import hashlib
import requests
import xmltodict
from dotenv import load_dotenv

load_dotenv()


class Subsonic:
    def __init__(self) -> None:
        self.url: str = (
            "http://192.168.1.102:8081/rest/"  # TODO: change the URL to container name
        )
        self.now: str = "getNowPlaying"
        self.get_song: str = "getSong"

    def get_song_info(self) -> dict:
        now_playing: dict = self.get_api(self.now, "")

        if not now_playing["subsonic-response"]["nowPlaying"]:
            return None

        song_id: dict = now_playing["subsonic-response"]["nowPlaying"]["entry"]["@id"]
        song_info: dict = self.get_api(self.get_song, song_id)
        return song_info

    def get_api(self, endpoint: str, song_id: str) -> dict:
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


sub = Subsonic()
print(sub.get_song_info())
