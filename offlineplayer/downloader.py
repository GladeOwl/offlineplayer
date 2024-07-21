import json
import logging
import os
from moviepy import editor

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from youtube_search import YoutubeSearch
from pytubefix import YouTube

from dotenv import load_dotenv

load_dotenv()

PATH: str = os.environ["SONG_FOLDER"]

LOGGER = logging.getLogger("reccy")


class Downloader:
    def __init__(self, songs: list) -> None:
        self.songs: list = songs

    def start_downloading(self) -> None:
        for song in self.songs:
            url: str = self.search_song(song)

            song_name: str = self.download_song(url=url)
            if not song_name:
                return

            song_path: str = f"./{PATH}/{song_name}.mp4"

            self.convert_mp4_to_mp3(file_path=song_path)
            # self.add_file_metadata(song=song)

    def search_song(self, song: str) -> str:
        search_string: str = f"{song['name']} {song['artist']}"
        results: list = YoutubeSearch(search_string, max_results=1).to_dict()

        if len(results) == 0:
            logging.error("No videos for the search parameter.")
            return None

        return results[0]["url_suffix"]

    def download_song(self, url: str) -> str:
        try:
            yt: YouTube = YouTube(url=url)
            stream = yt.streams.get_audio_only()
            logging.info(f"Downloading {yt.title} . . .")
            stream.download(output_path=PATH)
            logging.info(f"Finished Downloading {yt.title}")
            return yt.title
        except Exception as exc:
            logging.error(f"Downloaded failed: {exc}")
            print(f"Error {exc}")
            return None

    def convert_mp4_to_mp3(self, file_path: str) -> None:
        mp4_file: editor.AudioFileClip = editor.AudioFileClip(file_path)
        mp3_path: str = file_path.replace("mp4", "mp3")
        mp4_file.write_audiofile(mp3_path)
        mp4_file.close()
        os.remove(file_path)

    def add_file_metadata(self, song: dict) -> None:
        logging.info("Editing file metadata.")

        file_path: str = ""
        for file in os.listdir(path=PATH):
            if song["name"].lower() in file.lower():
                print(song["name"], file)
                file_path = os.path.join(PATH, file)
                break

        try:
            song_file = EasyID3(file_path)
        except ID3NoHeaderError:
            song_file = mutagen.File(file_path, easy=True)
            song_file.add_tags()

        print(song_file)

        song_file["title"] = song["name"]
        song_file["artist"] = song["artist"]
        song_file["album"] = song["album"]

        song_file.save()
