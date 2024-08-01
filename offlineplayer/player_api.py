import json
import os
import requests
import logging
from dotenv import load_dotenv

from models.session import Session
from models.song import Song

load_dotenv()

LOGGER = logging.getLogger("reccy")


class PlayerAPI:
    def __init__(self) -> None:
        self.url: str = os.environ["URL"]
        self.user_id: str = os.environ["USER_ID"]
        self.api_key: str = os.environ["API_KEY"]

        self.session: Session

    def api(
        self,
        endpoint: str,
        params: dict = {},
        headers: dict = {},
        json: dict = None,
        is_get: bool = True,
    ) -> dict:
        headers["X-Emby-Token"] = self.api_key
        params["userId"] = self.user_id

        if is_get:
            response: requests.Response = requests.get(
                url=self.url + endpoint, params=params, headers=headers, json=json
            )
        else:
            response: requests.Response = requests.post(
                url=self.url + endpoint, params=params, headers=headers, json=json
            )

        response.raise_for_status()

        if response.status_code == 204:
            return {"scan": True}

        return response.json()

    def get_session(self) -> Session:
        try:
            session_data: dict = self.api("Sessions")
        except Exception as exc:
            logging.error("Unable to get session data.")

        if "NowPlayingItem" not in session_data[0].keys():
            raise Exception("No song is playing")

        song_data: dict = session_data[0]["NowPlayingItem"]

        if not self.is_song_favorited(song_data["Id"]):
            logging.debug("Current song not favorited. Skipping it.")
            raise Exception("Current song not favorited. Skipping it.")

        song: Song = self.setup_song(song_data)

        self.session: Session = Session()
        self.session.id = session_data[0]["Id"]
        self.session.song = song
        self.session.queue = [item["Id"] for item in session_data[0]["NowPlayingQueue"]]

        return self.session

    def get_song(self, name: str) -> Song:
        params = {
            "searchTerm": name,
            "includeItemTypes": "Audio",
            "recursive": "true",
        }

        try:
            song_data: dict = self.api(f"Users/{self.user_id}/Items", params=params)
            return self.setup_song(song_data["Items"][0])
        except Exception as exc:
            logging.error(
                f"Could not find the song {name} with params : {params} :: {exc}"
            )
            raise

    def get_active_playlist(self) -> str:
        params: dict = {"IncludeItemTypes": "Playlist", "Recursive": "true"}
        session: Session = self.get_session()

        try:
            playlists: dict = self.api(f"Users/{self.user_id}/Items", params=params)
        except:
            logging.error("Could not get active playlist from the api.")
            raise

        for item in playlists["Items"]:
            # if item["ChildCount"] != len(session.queue):
            #     continue

            playlist: dict = self.api(f"Playlists/{item['Id']}/Items")

            count: int = 0
            for playlist_item in playlist["Items"]:
                if playlist_item["Id"] in session.queue:
                    count += 1

            if count == len(session.queue):
                return item

        logging.error("Could not find any active playlist")
        raise Exception("Could not find any active playlist")

    def add_song_to_playlist(self, song: Song) -> None:
        playlist: dict = self.get_active_playlist()

        song = self.get_song(song.name)
        logging.info(
            f"Adding song {song.name} ({song.player_id}) to playlist {playlist['Name']} ({playlist['Id']})"
        )
        params = {"ids": song.player_id}

        try:
            self.api(f"Playlists/{playlist['Id']}/Items", params=params, is_get=False)
            logging.info(f"Added {song.name} to {playlist['Name']}")
        except Exception as exc:
            LOGGER.error(
                f"Couldn't add the {song.name} to the playlist with these params: {params} :: {exc}"
            )
            raise

        params = {"ItemIds": song.player_id, "PlayCommand": "PlayLast"}
        self.api(f"Sessions/{self.session.id}/Playing", params=params, is_get=False)

        logging.info("Added song to queue.")

    def scan_library(self) -> dict:
        logging.info("Scanning Library")
        return self.api("/Library/Refresh", is_get=False)

    def setup_song(self, song_data: dict) -> Song:
        song: Song = Song()
        song.player_id = song_data["Id"]
        song.name = song_data["Name"]
        song.artist = song_data["Artists"]
        song.album = song_data["Album"]
        return song

    def is_song_favorited(self, id: str) -> bool:
        song: dict = PLAYERAPI.api(f"Items/{id}")
        return song["UserData"]["IsFavorite"]


PLAYERAPI = PlayerAPI()
