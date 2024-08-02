import logging
import requests

from spotify_api import SPOTIFYAPI
from models.recommendation import Recommendation
from models.song import Song

LOGGER = logging.getLogger("reccy")


def get_recommendations(song: Song, limit: int) -> list[Recommendation]:
    logging.info(f"Looking for recommendations for :: {song.name}")

    params: dict = {
        "seed_tracks": song.spotify_id,
        "seed_artists": song.artist_id,
        "limit": limit,
    }

    if song.genres:
        genres: str = ",".join(song.genres)
        params["seed_genres"] = genres
        logging.info(f"Found Genres: {genres}")

    try:
        response: dict = SPOTIFYAPI.get_api(endpoint="recommendations", params=params)
    except Exception as exc:
        logging.error("Could not get recommendations")
        raise exc

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
