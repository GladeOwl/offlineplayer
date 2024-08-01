import logging
from time import sleep

from spotify_api import SPOTIFYAPI
from player_api import PLAYERAPI
from downloader import DOWNLOADER
from recommendations import Recommendations
from classes.session import Session
from classes.song import Song

REC_LIMIT: int = 1


LOGGER = logging.getLogger("reccy")
logging.basicConfig(
    filename="/recommendations.log",
    encoding="utf-8",
    level=logging.INFO,
    format="[%(asctime)s] (%(filename)s) %(levelname)s :: %(message)s",
)


def main():
    reccy: Recommendations = Recommendations(limit=REC_LIMIT)

    session: Session = PLAYERAPI.get_session()
    if session == None:
        return

    song: Song = SPOTIFYAPI.get_song(session.song)
    if song == None:
        return

    songs: list = reccy.get_recommendations(song)

    for song in songs:
        DOWNLOADER.download_songs(song=song)
        PLAYERAPI.scan_library()
        sleep(2)  # give time to scan
        PLAYERAPI.add_song_to_playlist(song=song)


if __name__ == "__main__":
    logging.info("Starting reccy!")
    try:
        main()
    except Exception as exc:
        print(exc)
