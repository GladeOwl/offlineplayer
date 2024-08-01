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

    def api(
        self,
        endpoint: str,
        params: dict = None,
        headers: dict = {},
        is_get: bool = True,
    ) -> dict:
        headers["X-Emby-Token"] = self.api_key

        if is_get:
            response: requests.Response = requests.get(
                url=self.url + endpoint, params=params, headers=headers
            )
        else:
            response: requests.Response = requests.post(
                url=self.url + endpoint, params=params, headers=headers
            )

        if response.status_code <= 200 and response.status_code >= 299:
            raise Exception(
                f"Player API Status Code: {response.status_code}. Please check the issue."
            )

        if response.status_code == 204:
            return {"scan": True}

        return response.json()

    def get_session(self) -> Session:
        session_data: dict = self.api("Sessions")

        if session_data == None:
            logging.error("Unable to get session data.")
            return None

        if "NowPlayingItem" not in session_data[0].keys():
            raise Exception("No song is playing")

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

    def get_song_id(self, name: str) -> str:
        params = {
            "searchTerm": name,
            "includeItemTypes": "Audio",
            "recursive": "true",
        }

        try:
            song_data: dict = self.api(f"Users/{self.user_id}/Items", params=params)
            return song_data["Items"][0]["Id"]
        except Exception as exc:
            logging.error(
                f"Could not find the song {name} with params : {params} :: {exc}"
            )
            raise

    def is_song_favorited(self, id: str) -> bool:
        params: dict = {"userId": self.user_id}
        song: dict = PLAYERAPI.api(f"Items/{id}", params=params)
        return song["UserData"]["IsFavorite"]

    def get_active_playlist(self) -> str:
        params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
        session: Session = self.get_session()

        try:
            playlists: dict = self.api(f"Users/{self.user_id}/Items", params=params)
        except:
            logging.error("Could not get active playlist.")
            raise

        for item in playlists["Items"]:
            if item["ChildCount"] != len(session.queue):
                continue

            playlist: dict = self.api(
                f"Playlists/{item['Id']}/Items", params={"userId": self.user_id}
            )

            count: int = 0
            for playlist_item in playlist["Items"]:
                if playlist_item["Id"] in session.queue:
                    count += 1

            if count == len(session.queue):
                return item["Items"][0]

    def scan_library(self) -> dict:
        logging.info("Scanning Library")
        return self.api("/Library/Refresh", is_get=False)

    def add_song_to_playlist(self, song: Song) -> None:
        song_id: str = self.get_song_id(song.name)
        params = {"userId": self.user_id, "ids": song_id}
        playlist: dict = self.get_active_playlist()

        try:
            self.api(f"Playlists/{playlist['Id']}/Items", params=params)
            logging.info(f"Added {song.name} to {playlist['Name']}")
        except Exception as exc:
            LOGGER.error(
                f"Couldn't add the {song.name} to the playlist with these params: {params} :: {exc}"
            )
            raise


PLAYERAPI = PlayerAPI()
