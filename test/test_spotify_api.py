import os
import sys
import json

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../offlineplayer"))
)

from spotify_api import SPOTIFYAPI
from classes.song import Song


def test_get_song():
    song: Song = Song()
    song.name = "Keeping Everything Inside"
    song.album = "Keeping Everything Inside"
    song.artist = "Sophie Pecora"

    response: dict = SPOTIFYAPI.get_song(song)
    with open("offlineplayer/data/search.json", "w") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_genres():
    song_id: str = "5GyjS2wRsmuoCjtI8TA2Yn"
    response: dict = SPOTIFYAPI.get_genres(song_id)
    with open("offlineplayer/data/album.json", "w+") as jsonf:
        json.dump(response, jsonf)

    assert response != None
