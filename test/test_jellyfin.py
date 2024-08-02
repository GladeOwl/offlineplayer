from offlineplayer.player_api import PLAYERAPI


def test_scan():
    response: dict = PLAYERAPI.scan_library()
    assert response != None
