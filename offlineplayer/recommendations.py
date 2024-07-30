import logging
import requests

from spotify_api import SPOTIFYAPI
from player_api import PLAYERAPI
from classes.recommendation import Recommendation
from classes.session import Session
from classes.song import Song

LOGGER = logging.getLogger("reccy")


class Recommendations:
    def __init__(self, limit: int = 10) -> None:
        self.song: Song
        self.session: Session
        self.limit: int = limit

    def start_process(self) -> None:
        self.session = PLAYERAPI.get_session()

        if self.session == None:
            return None

        # TODO: Only recommend if song is favourited.
        self.song = SPOTIFYAPI.get_song(self.session.song)

        if self.song == None:
            return None

    def get_recommendations(self, song: Song) -> list[Recommendation]:
        genres: str = ",".join(song.genres)
        logging.info(f"Logging for recommendations. Genres: {genres}")

        params: dict = {
            "seed_tracks": song.spotify_id,
            "seed_artists": song.artist_id,
            "seed_genres": genres,
            "limit": self.limit,
        }

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


RECOMMENDATIONS = Recommendations()
