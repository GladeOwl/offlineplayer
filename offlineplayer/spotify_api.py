import os
import requests
import urllib
import json
import logging

from api_token import TOKEN
from classes.song import Song
from dotenv import load_dotenv

load_dotenv()
LOGGER = logging.getLogger("reccy")


class Spotify_API:
    def __init__(self) -> None:
        self.url: str = os.environ["SPOTIFY_URL"]
        self.token = TOKEN.token

    def get_api(self, endpoint: str, params: dict = {}) -> dict:
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

    def get_song(self, song: Song) -> Song:
        q: str = self.encode_params(song)
        params: dict = {"q": q, "type": song.type, "limit": 10}

        logging.info(f"Looking for {song.name} with params: {q}")

        search_data: dict = self.get_api(endpoint="search", params=params)

        with open("offlineplayer/data/raw_search1.json", "w") as jsonf:
            json.dump(search_data, jsonf, indent=4)

        for track in search_data["tracks"]["items"]:
            if (
                track["name"].lower() in song.name.lower()
                and track["album"]["name"].lower() in song.album.lower()
            ):
                logging.info(f"Found Song on Spotify:")
                logging.info(
                    f"Local - {song.name} by {song.artist} :: Spotify - {track['name']} by {track['artists'][0]['name']} :: {track['external_urls']['spotify']}"
                )

                song.spotify_id = track["id"]
                song.artist_id = track["artists"][0]["id"]
                song.album_id = track["album"]["id"]
                song.genres = self.get_genres(song.album_id)
                return song

        logging.error(f"No song found matching the name : {q}")
        return None

    def get_genres(self, id: str) -> list:
        response: dict = self.get_api(endpoint=f"albums/{id}")
        with open("offlineplayer/data/raw_albums1.json", "w") as jsonf:
            json.dump(response, jsonf, indent=4)

        if response == None:
            logging.error("No genres found.")
            return None

        return response["genres"]


SPOTIFYAPI = Spotify_API()
