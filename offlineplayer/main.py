import logging
import time
from recommendations import Recommendations
from downloader import Downloader

REC_PER_SONG: int = 1

REC: Recommendations = Recommendations(REC_PER_SONG)

LOGGER = logging.getLogger("reccy")
logging.basicConfig(
    filename="/recommendations.log",
    encoding="utf-8",
    level=logging.INFO,
    format="[%(asctime)s] (%(filename)s) %(levelname)s :: %(message)s",
)

if __name__ == "__main__":
    try:
        songs: list = REC.get_recommendations()
        if songs != None:
            downloader: Downloader = Downloader(songs=songs)
            downloader.start_downloading()
    except Exception as exc:
        print(exc)
