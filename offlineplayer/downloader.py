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

from classes.recommendation import Recommendation
from classes.song import Song

load_dotenv()

FOLDER: str = os.environ["INTERNAL_SONG_PATH"]

LOGGER = logging.getLogger("reccy")


class Downloader:
    def download_songs(self, songs: list) -> None:
        for song in songs:
            url: str = self.get_url(song)

            song_name: str = self.download(url=url)
            if not song_name:
                continue

            song_path: str = os.path.join(FOLDER, f"{song_name}.mp4")

            self.convert_mp4_to_mp3(file_path=song_path)
            self.add_file_metadata(song=song)

    def get_url(self, song: Song) -> str:
        search_string: str = f"{song.name} {song.artist_name}"
        results: list = YoutubeSearch(search_string, max_results=1).to_dict()

        if len(results) == 0:
            logging.error("No videos for the search parameter.")
            return None

        return results[0]["url_suffix"]

    def download(self, url: str) -> str:
        try:
            yt: YouTube = YouTube(url=url)
            stream = yt.streams.get_audio_only()
            logging.info(f"Downloading {yt.title} . . .")
            stream.download(output_path=FOLDER)
            logging.info(f"Finished Downloading {yt.title}")
            return yt.title
        except Exception as exc:
            logging.error(f"Downloaded failed: {exc}")
            print(f"Download Error :: {exc}")
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
        for file in os.listdir(path=FOLDER):
            if song.name.lower() in file.lower():
                file_path = os.path.join(FOLDER, file)
                break

        try:
            song_file = EasyID3(file_path)
        except ID3NoHeaderError:
            song_file = mutagen.File(file_path, easy=True)
            song_file.add_tags()

        song_file["title"] = song.name
        song_file["artist"] = song.artist_name
        song_file["album"] = song.album_name

        song_file.save()

        logging.info("File Metadata added")


DOWNLOADER = Downloader()
