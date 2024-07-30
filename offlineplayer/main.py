import logging

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
    song: Song = SPOTIFYAPI.get_song(session.song)
    songs: list = reccy.get_recommendations(song)

    if songs == None:
        logging.error(
            "No songs were found for downloading. Something must've gone wrong!"
        )
        return

    DOWNLOADER.download_songs(songs=songs)


if __name__ == "__main__":
    logging.info("Starting reccy!")
    main()
