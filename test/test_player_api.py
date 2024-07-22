import pytest
import json
from ..offlineplayer.player_api import PLAYERAPI


def test_api_ping():
    response: dict = PLAYERAPI.get_api("System/Ping")
    assert response != None


def test_get_session():
    response: dict = PLAYERAPI.get_api("Sessions")
    with open("offlineplayer/data/session.json", "w+") as jsonf:
        json.dump(response, jsonf, indent=4)

    assert response != None
