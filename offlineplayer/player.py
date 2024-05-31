import os
import time
import simpleaudio
from pydub import AudioSegment
from rich.progress import Progress
from queue import Queue

FOLDER: str = "D:\\Music\\Backup\\"


class Player:
    def __init__(self, queue: Queue) -> None:
        self.queue: Queue = queue
        self.next_track()

    def next_track(self) -> None:
        self.current_track: str = self.queue.next_track()
        self.current_track_path: str = os.path.join(self.queue.path, self.current_track)
        self.track: AudioSegment = AudioSegment.from_mp3(self.current_track_path)
        self.play()

    def play(self) -> None:
        self.play_obj: simpleaudio.PlayObject = simpleaudio.play_buffer(
            audio_data=self.track.raw_data,
            num_channels=self.track.channels,
            bytes_per_sample=self.track.sample_width,
            sample_rate=self.track.frame_rate,
        )

        self.progress()
        self.play_obj.wait_done()
        self.next_track()

    def progress(self) -> None:
        self.start_time: float = time.time()

        with Progress() as progress:
            task = progress.add_task(
                f"[green] {self.current_track}", total=self.track.duration_seconds
            )
            while self.play_obj.is_playing():
                elapsed_time = time.time() - self.start_time
                progress.update(task, completed=elapsed_time)
                time.sleep(1)


if __name__ == "__main__":
    queue: Queue = Queue(FOLDER)
    player: Player = Player(queue)
