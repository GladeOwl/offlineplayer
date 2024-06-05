import logging
import requests
import json

from search import Search
from subsonic_api import SUBSONIC
from api_token import TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="recommendations.log", encoding="utf-8", level=logging.INFO
)


class Song:
    id: str
    name: str
    album: str
    artist: str


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

        recommendations: dict = self.get_recommendations(search_data)
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

        search_response: dict = search.search()

        for song in search_response["tracks"]["items"]:
            if (
                song["name"].lower() == self.song.name.lower()
                and song["album"]["name"].lower() == self.song.album.lower()
            ):
                logging.info(f"Found Song on Spotify:")
                logging.info(
                    f"Local - {self.song.name} by {self.song.artist} :: Spotify - {song['name']} by {song['artists'][0]['name']} :: {song['external_urls']['spotify']}"
                )
                return {"song_id": song["id"], "artists_id": song["artists"][0]["id"]}

    def get_recommendations(self, search_data: dict) -> None:
        logging.info(f"Looking for recommendations")

        url: str = "https://api.spotify.com/v1/recommendations"
        headers: dict = {"Authorization": f"Bearer {TOKEN.token}"}
        params: dict = {
            "seed_tracks": search_data["song_id"],
            "seed_artists": search_data["artists_id"],
            "seed_genres": "neo-singer-songwriter",
        }

        response: requests.Response = requests.get(url, headers=headers, params=params)

        with open("rec.json", "w") as jsonf:
            json.dump(response.json(), jsonf, indent=4)

        return response.json()

    def parse_recommendations(self, recommendations: dict) -> None:
        for rec in recommendations["tracks"]:
            print(rec["album"]["name"] + " " + rec["album"]["external_urls"]["spotify"])


REC = Recommendations()
REC.start_sequence()
