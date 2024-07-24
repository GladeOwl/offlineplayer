import os
import requests
import urllib
import json
import logging

from api_token import TOKEN
from helper import api_get
from song import Song

LOGGER = logging.getLogger("reccy")


class Spotify_API:
    def __init__(self, song: Song) -> None:
        self.url: str = os.environ["SPOTIFY_URL"]
        self.token = TOKEN.token

    def get_api(self, endpoint: str, params: dict) -> requests.Response:
        headers: dict = {"Authorization": f"Bearer {TOKEN.token}"}

        response: requests.Response = requests.get(
            url=self.url + endpoint, headers=headers, params=params
        )

        if response.status_code != 200:
            logging.error(
                f"Spotify API Status Code: {response.status_code}. Please check the issue."
            )
            return None

        return response.json()

    def encode_params(self, song: Song) -> str:
        data: dict = {
            "artist": song.artist,
            "track": song.name,
        }
        return urllib.parse.urlencode(data)

    def get_song(self, song: Song) -> dict:
        q: str = self.encode_params(song)
        params: dict = {"q": q, "type": song.type, "limit": 10}

        logging.info(f"Looking for {song.name} with params: {q}")

        response: requests.Response = self.get_api(endpoint="search", params=params)

        with open("search.json", "w") as jsonf:  # TODO: Remove in production
            json.dump(response.json(), jsonf, indent=4)

        for track in response.json()["tracks"]["items"]:
            if (
                track["name"].lower() in song.name.lower()
                and track["album"]["name"].lower() in song.album.lower()
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

        logging.error(f"No song found matching the name : {q}")
        return None


SPOTIFYAPI = Spotify_API()
