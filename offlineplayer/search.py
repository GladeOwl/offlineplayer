import requests
import urllib
import json

from helper import api_get


class Search:
    def __init__(self, track: str, artist: str, album: str, type: str) -> None:
        self.track: str = track
        self.artist: str = artist
        self.album: str = album
        self.type: str = type

    def encode_params(self) -> None:
        data: dict = {"track": self.track, "artist": self.artist, "album": self.album}
        return urllib.parse.urlencode(data)

    def search(self) -> dict:
        params: dict = {"q": self.encode_params(), "type": self.type, "limit": 2}
        response: requests.Response = api_get(endpoint="search", params=params)

        with open("search.json", "w") as jsonf:
            json.dump(response.json(), jsonf, indent=4)

        return response.json()
