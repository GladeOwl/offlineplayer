import logging
import requests

from spotify_api import SPOTIFYAPI
from player_api import PLAYERAPI
from session import Session
from song import Song

LOGGER = logging.getLogger("reccy")


class Recommnedations:
    def __init__(self) -> None:
        self.song: Song

    def get_recommendations(self) -> None:
        session: Session = PLAYERAPI.get_session()

        if session == None:
            return None

        # TODO: Only recommend if song is favourited.
        self.song = session.song
        search_data: dict = self.search_song()

    def search_song(self) -> None: ...
    def get_genres(self) -> None: ...
