import requests
import urllib
import json
import logging

from helper import api_get
from song import Song

LOGGER = logging.getLogger("reccy")


class Search:
    def __init__(self, song: Song) -> None:
        self.song: Song = song

    def encode_params(self) -> str:
        data: dict = {
            "artist": self.song.artist,
            "track": self.song.name,
        }
        return urllib.parse.urlencode(data)

    def search(self) -> dict:
        q: str = self.encode_params()
        params: dict = {"q": q, "type": self.song.type, "limit": 10}
        logging.info(f"Looking with params: {q}")

        response: requests.Response = api_get(endpoint="search", params=params)

        with open(
            "./offlineplayer/data/search.json", "w"
        ) as jsonf:  # TODO: Remove in production
            json.dump(response.json(), jsonf, indent=4)

        for track in response.json()["tracks"]["items"]:
            if (
                track["name"].lower() in self.song.name.lower()
                and track["album"]["name"].lower() in self.song.album.lower()
            ):
                logging.info(f"Found Song on Spotify:")
                logging.info(
                    f"Local - {self.song.name} by {self.song.artist} :: Spotify - {track['name']} by {track['artists'][0]['name']} :: {track['external_urls']['spotify']}"
                )

                return {
                    "song_id": track["id"],
                    "artists_id": track["artists"][0]["id"],
                    "album_id": track["album"]["id"],
                }

        logging.error(f"No song found matching the name : {q}")
        return None
