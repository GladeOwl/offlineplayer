import os
import sys
import json

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../offlineplayer"))
)

from player_api import PLAYERAPI
from session import Session


def test_api_ping():
    response: dict = PLAYERAPI.get_api("System/Ping")
    assert response != None


def test_get_session_from_api():
    response: dict = PLAYERAPI.get_api("Sessions")
    with open("offlineplayer/data/session.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_session_from_class():
    session: Session = PLAYERAPI.get_session()
    print(session.queue)

    assert session != None


def test_get_playlists():
    params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
    response: dict = PLAYERAPI.get_api(f"Users/{PLAYERAPI.user_id}/Items", params)
    with open("offlineplayer/data/playlists.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_playlist():
    params: dict = {"userId": PLAYERAPI.user_id}
    playlist_id: str = "81fa3a83-5fd0-d0ab-705c-fbf40d0e223c"
    response: dict = PLAYERAPI.get_api(f"Playlists/{playlist_id}/Items", params=params)

    with open("offlineplayer/data/playlist.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None
