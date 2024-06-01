import requests
import urllib
import json
from api_token import TOKEN


class Search:
    def __init__(self, track: str, artist: str, album: str, type: str) -> None:
        self.track: str = track
        self.artist: str = artist
        self.album: str = album
        self.type: str = type

    def encode_params(self) -> None:
        data: dict = {"track": self.track, "artist": self.artist, "album": self.album}
        return urllib.parse.urlencode(data)

    def search(self) -> None:
        url: str = "https://api.spotify.com/v1/search"
        headers: dict = {"Authorization": f"Bearer {TOKEN.token}"}
        params: dict = {"q": self.encode_params(), "type": self.type, "limit": 2}
        response: requests.Response = requests.get(url, headers=headers, params=params)
        print(response.url)
        with open("search.json", "w") as jsonf:
            json.dump(response.json(), jsonf, indent=4)


search = Search(
    track="King",
    artist="Lauren Aquilina",
    album="Fools",
    type="track",
)
search.search()
