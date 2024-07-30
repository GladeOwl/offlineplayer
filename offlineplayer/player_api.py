import os
import requests
import logging
from dotenv import load_dotenv

from classes.session import Session
from classes.song import Song

load_dotenv()

LOGGER = logging.getLogger("reccy")


class PlayerAPI:
    def __init__(self) -> None:
        self.url: str = os.environ["URL"]
        self.user_id: str = os.environ["USER_ID"]
        self.api_key: str = os.environ["API_KEY"]

    def get_api(self, endpoint: str, params: dict = None, headers: dict = {}) -> dict:
        headers["X-Emby-Token"] = self.api_key

        response: requests.Response = requests.get(
            url=self.url + endpoint, params=params, headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f"Player API Status Code: {response.status_code}. Please check the issue."
            )
            return None

        return response.json()

    def get_session(self) -> Session:
        session_data: dict = self.get_api("Sessions")

        if session_data == None:
            logging.error("Unable to get session data.")
            return None

        if session_data[0]["NowPlayingItem"] == None:
            logging.debug("No song is playing.")
            return None

        song_data: dict = session_data[0]["NowPlayingItem"]

        if not self.is_song_favorited(song_data["Id"]):
            logging.debug("Current song not favorited. Skipping it.")
            return None

        song: Song = Song()
        song.player_id = song_data["Id"]
        song.name = song_data["Name"]
        song.artist = song_data["Artists"]
        song.album = song_data["Album"]

        session: Session = Session()
        session.song = song
        session.queue = [item["Id"] for item in session_data[0]["NowPlayingQueue"]]

        return session

    def is_song_favorited(self, id: str) -> bool:
        params: dict = {"userId": PLAYERAPI.user_id}
        song: dict = PLAYERAPI.get_api(f"Items/{id}", params=params)
        return song["UserData"]["IsFavorite"]

    def get_active_playlist(self) -> str:
        params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
        playlists: dict = self.get_api(f"Users/{self.user_id}/Items", params=params)
        session: Session = self.get_session()

        for item in playlists["Items"]:
            if item["ChildCount"] != len(session.queue):
                continue

            playlist: dict = self.get_api(
                f"Playlists/{item['Id']}/Items", params={"userId": self.user_id}
            )

            count: int = 0
            for playlist_item in playlist["Items"]:
                if playlist_item["Id"] in session.queue:
                    count += 1

            if count == len(session.queue):
                return item["Id"]

    def scan_library(self) -> dict:
        return self.get_api("/Library/Refresh")

    # def add_song_to_playlist(self) -> None:


PLAYERAPI = PlayerAPI()
