import logging
import requests

from spotify_api import SPOTIFYAPI
from player_api import PLAYERAPI
from classes.recommendation import Recommendation
from classes.song import Song

LOGGER = logging.getLogger("reccy")


class Recommendations:
    def __init__(self, limit: int = 10) -> None:
        self.song: Song
        self.limit: int = limit

    def get_recommendations(self, song: Song) -> list[Recommendation]:
        logging.info(f"Looking for recommendations for :: {song.name}")

        params: dict = {
            "seed_tracks": song.spotify_id,
            "seed_artists": song.artist_id,
            "limit": self.limit,
        }

        if song.genres:
            genres: str = ",".join(song.genres)
            params["seed_genres"] = genres
            logging.info(f"Found Genres: {genres}")

        response: requests.Response = SPOTIFYAPI.get_api(
            endpoint="recommendations", params=params
        )

        recommendations: list = []

        for recommendation in response["tracks"]:
            song: Recommendation = Recommendation()
            song.name = recommendation["name"]
            song.artist_name = recommendation["artists"][0]["name"]
            song.artist_id = recommendation["artists"][0]["id"]
            song.album_name = recommendation["album"]["name"]
            song.album_id = recommendation["album"]["id"]

            recommendations.append(song)

        return recommendations
