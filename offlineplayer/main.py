import logging
import traceback

from time import sleep

from spotify_api import SPOTIFYAPI
from player_api import PLAYERAPI
from downloader import DOWNLOADER
from recommendations import get_recommendations
from models.session import Session
from models.song import Song

REC_LIMIT: int = 1


LOGGER = logging.getLogger("reccy")
logging.basicConfig(
    filename="/recommendations.log",
    encoding="utf-8",
    level=logging.INFO,
    format="[%(asctime)s] (%(filename)s) %(levelname)s :: %(message)s",
)


def main():
    try:
        session: Session = PLAYERAPI.get_session()
        PLAYERAPI.get_active_playlist()
    except Exception as exc:
        raise exc

    song: Song = SPOTIFYAPI.get_song(session.song)
    songs: list = get_recommendations(song, REC_LIMIT)

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
        traceback.print_exc()
