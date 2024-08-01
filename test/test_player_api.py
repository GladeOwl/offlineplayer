import os
import sys
import json
from urllib.parse import quote


from offlineplayer.player_api import PLAYERAPI
from offlineplayer.classes.session import Session


def test_api_ping():
    response: dict = PLAYERAPI.api("System/Ping")
    assert response != None


def test_get_session_from_api():
    response: dict = PLAYERAPI.api("Sessions")
    with open("offlineplayer/data/session.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_session_from_class():
    session: Session = PLAYERAPI.get_session()
    assert session != None


def test_get_playlists():
    params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
    response: dict = PLAYERAPI.api(f"Users/{PLAYERAPI.user_id}/Items", params)
    with open("offlineplayer/data/playlists.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_playlist():
    params: dict = {"userId": PLAYERAPI.user_id}
    playlist_id: str = "b754a3fd06f8da79cbae74575df78238"
    response: dict = PLAYERAPI.api(f"Playlists/{playlist_id}/Items", params=params)

    with open("offlineplayer/data/playlist.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_active_playlist():
    playlist_id: str = PLAYERAPI.get_active_playlist()
    assert playlist_id != None


def test_get_song_from_api_with_session():
    session: dict = PLAYERAPI.api("Sessions")
    song_id: str = session[0]["NowPlayingItem"]["Id"]

    params: dict = {"userId": PLAYERAPI.user_id}
    song: dict = PLAYERAPI.api(f"Items/{song_id}", params=params)

    assert song != None


def test_find_song_from_api():
    name: str = "Nothing’s Gonna Stop Me Now"
    params = {
        "searchTerm": quote(name),
        "includeItemTypes": "Audio",
        "recursive": "true",
    }

    response: dict = PLAYERAPI.api(f"Users/{PLAYERAPI.user_id}/Items", params=params)

    with open("offlineplayer/data/song.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response["Items"] != None
