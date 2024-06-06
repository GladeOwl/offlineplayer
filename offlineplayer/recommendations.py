import logging
import requests
import json

from helper import api_get
from search import Search
from subsonic_api import SUBSONIC
from song import Song

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="recommendations.log", encoding="utf-8", level=logging.INFO
)


class Recommendations:
    def __init__(self) -> None:
        self.song: Song = None

    def start_sequence(self) -> None:
        if not SUBSONIC.is_playing():
            logging.info("No song playing.")
            return

        song_info: dict = SUBSONIC.get_song_info()
        if not self.is_song_starred(song_info):
            logging.info("Current Playing song is not starred.")
            return

        self.song = self.create_song(song_info)
        search_data: dict = self.search_song()

        genres: str = self.get_genres(search_data["album_id"])

        recommendations: dict = self.get_recommendations(search_data, genres)
        self.parse_recommendations(recommendations)

    def is_song_starred(self, song_info: dict) -> bool:
        return True if "@starred" in song_info["subsonic-response"]["song"] else False

    def create_song(self, song_info: dict) -> Song:
        song: Song = Song()
        song.name = song_info["subsonic-response"]["song"]["@title"]
        song.album = song_info["subsonic-response"]["song"]["@album"]
        song.artist = song_info["subsonic-response"]["song"]["@artist"]

        return song

    def search_song(self) -> dict:
        logging.info(f"Looking for '{self.song.name}' on Spotify:")

        search: Search = Search(
            track=self.song.name,
            artist=self.song.artist,
            album=self.song.album,
            type="track",
        )

        return search.search(song=self.song)

    def get_genres(self, id: str) -> str:
        endpoint: str = "albums/" + id
        response: requests.Response = api_get(endpoint=endpoint, params={})
        with open("album.json", "w+") as jsonf:
            json.dump(response.json(), jsonf)

        return ",".join(response.json()["genres"])

    def get_recommendations(self, search_data: dict, genres: str) -> dict:
        logging.info(f"Looking for recommendations. Genres: {genres}")

        params: dict = {
            "seed_tracks": search_data["song_id"],
            "seed_artists": search_data["artists_id"],
            "seed_genres": genres,
        }
        response: requests.Response = api_get(endpoint="recommendations", params=params)

        with open("rec.json", "w") as jsonf:
            json.dump(response.json(), jsonf, indent=4)

        return response.json()

    def parse_recommendations(self, recommendations: dict) -> None:
        for rec in recommendations["tracks"]:
            print(rec["album"]["name"] + " " + rec["album"]["external_urls"]["spotify"])


REC = Recommendations()
REC.start_sequence()
