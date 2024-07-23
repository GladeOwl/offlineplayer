import os
import requests
import logging

from session import Session
from song import Song
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("reccy")


class PlayerAPI:
    def __init__(self) -> None:
        self.url: str = os.environ["URL"]
        self.user_id: str = os.environ["USER_ID"]
        self.api_key: str = os.environ["API_KEY"]
        self.active_playlist_id: str

    def get_api(self, endpoint: str, params: dict = None, headers: dict = {}) -> dict:
        headers["X-Emby-Token"] = self.api_key

        response: requests.Response = requests.get(
            url=self.url + endpoint, params=params, headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f"API Status Code: {response.status_code}. Please check the issue."
            )
            return None

        return response.json()

    def get_session(self) -> Session:
        session_data: dict = self.get_api("Sessions")
        if session_data == None:
            return None

        song_data: dict = session_data[0]["NowPlayingItem"]

        song: Song = Song()
        song.name = song_data["Name"]
        song.artist = song_data["Artists"]
        song.album = song_data["Album"]

        session: Session = Session()
        session.song = song
        session.queue = [x["Id"] for x in session_data[0]["NowPlayingQueue"]]

        return session

    def get_active_playlist(self) -> None:
        params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
        playlists: dict = self.get_api(f"Users/{self.user_id}/Items", params)
        session: Session = self.get_session()

        for item in playlists["Items"]:
            if item["ChildCount"] != len(session.queue):
                continue

            _params: dict = {"userId": self.user_id}
            playlist: dict = self.get_api(
                f"Playlist/{item['id']}/Items", params=_params
            )

            count: int = 0
            # for playlist_item in playlist["Items"]:
            #     if playlist_item["Id"] ==


PLAYERAPI = PlayerAPI()
