import pytest
import os
import sys
import json

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../offlineplayer"))
)

from player_api import PLAYERAPI
from spotify_api import SPOTIFYAPI
from recommendations import RECOMMENDATIONS
from classes.recommendation import Recommendation
from classes.song import Song


def test_recommendations():
    session = PLAYERAPI.get_session()
    song = SPOTIFYAPI.get_song(session.song)
    recommendations: list = RECOMMENDATIONS.get_recommendations(song)
    with open("offlineplayer/data/recommendations.json", "w+") as jsonf:
        json.dump(recommendations, jsonf)

    assert recommendations != None
