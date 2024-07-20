import os
import logging
import requests
import json
from time import time

from helper import api_get
from search import Search
from subsonic_api import SUBSONIC
from song import Song

LOGGER = logging.getLogger("reccy")


class Recommendations:
    def __init__(self, rec_limit: int) -> None:
        self.song: Song = None
        self.rec_limit = rec_limit

    def get_recommendations(self) -> list:
        if not SUBSONIC.is_playing():
            logging.info("No song playing.")
            return None

        song_info: dict = SUBSONIC.get_song_info()
        if not self.is_song_starred(song_info):
            logging.info("Current Playing song is not starred.")
            return None

        self.song = self.create_song(song_info)
        search_data: dict = self.search_song()

        if search_data == None:
            logging.error("No data found. No recommends.")
            return None

        genres: str = self.get_genres(search_data["album_id"])

        recommendations: dict = self.get_rec_from_api(search_data, genres)

        self.make_note_of_song(search_data)
        return self.parse_recommendations(recommendations)

    def is_song_starred(self, song_info: dict) -> bool:
        return True if "@starred" in song_info["subsonic-response"]["song"] else False

    def create_song(self, song_info: dict) -> Song:
        song: Song = Song()
        song.name = song_info["subsonic-response"]["song"]["@title"]
        song.album = song_info["subsonic-response"]["song"]["@album"]
        song.artist = song_info["subsonic-response"]["song"]["@artist"]
        song.type = "track"

        return song

    def search_song(self) -> dict:
        logging.info(f"Looking for '{self.song.name}' on Spotify:")
        search: Search = Search(self.song)
        search_data: dict = search.search()
        self.song.id = search_data["song_id"]

        return search_data

    def get_genres(self, id: str) -> str:
        endpoint: str = "albums/" + id
        response: requests.Response = api_get(endpoint=endpoint, params={})

        with open("album.json", "w+") as jsonf:  # TODO: Remove in production
            json.dump(response.json(), jsonf)

        return ",".join(response.json()["genres"])

    def get_rec_from_api(self, search_data: dict, genres: str) -> dict:
        logging.info(f"Looking for recommendations. Genres: {genres}")

        params: dict = {
            "seed_tracks": search_data["song_id"],
            "seed_artists": search_data["artists_id"],
            "seed_genres": genres,
            "limit": self.rec_limit,
        }
        response: requests.Response = api_get(endpoint="recommendations", params=params)

        with open("rec.json", "w") as jsonf:  # TODO: Remove in production
            json.dump(response.json(), jsonf, indent=4)

        return response.json()

    def parse_recommendations(self, recommendations: dict) -> list:
        rec_list: list = []
        for rec in recommendations["tracks"]:
            print(
                f"{rec['name']} by {rec['artists'][0]['name']} :: {rec['album']['external_urls']['spotify']}"
            )
            song_data: dict = {
                "name": rec["name"],
                "artist": rec["artists"][0]["name"],
                "album": rec["album"]["name"],
            }
            rec_list.append(song_data)
        return rec_list

    def make_note_of_song(self, search_data: dict) -> None:
        note: dict = {
            "name": self.song.name,
            "id": self.song.id,
            "album": {"name": self.song.album, "id": search_data["album_id"]},
            "artist": {"name": self.song.artist, "id": search_data["artists_id"]},
            "last_recommended": time(),
        }

        with open("history.json", "w+") as jsonf:
            if os.path.getsize("history.json") == 0:
                json.dump([note], jsonf, indent=4)
                return

            history: list = json.load(jsonf)

            found_note: bool = False
            for _note in history:
                if _note["name"] == self.song.name:
                    _note = note
                    found_note = True

            if not found_note:
                history.append(note)

            json.dump(history, jsonf, indent=4)
