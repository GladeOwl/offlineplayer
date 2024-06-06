import requests
import urllib
import json
import logging

from helper import api_get
from song import Song

logging.basicConfig(
    filename="recommendations.log", encoding="utf-8", level=logging.INFO
)


class Search:
    def __init__(self, track: str, artist: str, album: str, type: str) -> None:
        self.track: str = track
        self.artist: str = artist
        self.album: str = album
        self.type: str = type

    def encode_params(self) -> str:
        data: dict = {"track": self.track, "artist": self.artist, "album": self.album}
        return urllib.parse.urlencode(data)

    def search(self, song: Song) -> dict:
        params: dict = {"q": self.encode_params(), "type": self.type, "limit": 2}
        response: requests.Response = api_get(endpoint="search", params=params)

        with open("search.json", "w") as jsonf:
            json.dump(response.json(), jsonf, indent=4)

        for track in response.json()["tracks"]["items"]:
            if (
                track["name"].lower() == song.name.lower()
                and track["album"]["name"].lower() == song.album.lower()
            ):
                logging.info(f"Found Song on Spotify:")
                logging.info(
                    f"Local - {song.name} by {song.artist} :: Spotify - {track['name']} by {track['artists'][0]['name']} :: {track['external_urls']['spotify']}"
                )

                return {
                    "song_id": track["id"],
                    "artists_id": track["artists"][0]["id"],
                    "album_id": track["album"]["id"],
                }
