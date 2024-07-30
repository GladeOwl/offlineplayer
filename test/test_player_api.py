import os
import sys
import json
import pytest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../offlineplayer"))
)

from player_api import PLAYERAPI
from classes.session import Session


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
    assert session != None


def test_get_playlists():
    params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
    response: dict = PLAYERAPI.get_api(f"Users/{PLAYERAPI.user_id}/Items", params)
    with open("offlineplayer/data/playlists.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


def test_get_playlist():
    params: dict = {"userId": PLAYERAPI.user_id}
    playlist_id: str = "b754a3fd06f8da79cbae74575df78238"
    response: dict = PLAYERAPI.get_api(f"Playlists/{playlist_id}/Items", params=params)

    with open("offlineplayer/data/playlist.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None


@pytest.mark.xfail(
    reason="The specific playlist should be playing for this test to pass"
)
def test_active_playlist():
    reference_id: str = "b754a3fd06f8da79cbae74575df78238"
    active_id: str = PLAYERAPI.get_active_playlist()
    assert reference_id == active_id


def test_get_song_from_api():
    session: dict = PLAYERAPI.get_api("Sessions")
    song_id: str = session[0]["NowPlayingItem"]["Id"]

    params: dict = {"userId": PLAYERAPI.user_id}
    song: dict = PLAYERAPI.get_api(f"Items/{song_id}", params=params)

    assert song != None
