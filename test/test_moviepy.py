import pytest
import os
from moviepy import editor


def test_moviepy():
    path: str = "offlineplayer\music"
    for song in os.listdir(path):
        if ".mp4" not in song:
            continue

        mp4_path: str = path + "\\" + song
        mp4_file: editor.AudioFileClip = editor.AudioFileClip(mp4_path)
        mp3_path: str = mp4_path.replace("mp4", "mp3")
        mp4_file.write_audiofile(mp3_path)
        mp4_file.close()
