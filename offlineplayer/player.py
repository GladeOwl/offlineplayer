import os
import time
import simpleaudio
from pydub import AudioSegment
from rich.progress import Progress
from song_queue import Song_Queue

FOLDER: str = "D:\\Music\\Backup\\"


class Player:
    def __init__(self, queue: Song_Queue) -> None:
        self.queue: Song_Queue = queue
        self.current_track: str = None
        self.current_track_path: str = None
        self.track: AudioSegment = None
        self.play_obj: simpleaudio.PlayObject = None
        self.start_time: float = None

    def run(self) -> None:
        while True:
            self.next_track()
            self.start_track()
            self.track_progress()

    def next_track(self) -> None:
        self.current_track = self.queue.next_track()
        self.current_track_path = os.path.join(self.queue.path, self.current_track)
        self.track = AudioSegment.from_mp3(self.current_track_path)

    def start_track(self) -> None:
        self.play_obj = simpleaudio.play_buffer(
            audio_data=self.track.raw_data,
            num_channels=self.track.channels,
            bytes_per_sample=self.track.sample_width,
            sample_rate=self.track.frame_rate,
        )

    def track_progress(self) -> None:
        self.start_time = time.time()

        with Progress() as progress:
            task = progress.add_task(
                f"[green] {self.current_track}", total=self.track.duration_seconds
            )
            while self.play_obj.is_playing():
                elapsed_time = time.time() - self.start_time
                progress.update(task, completed=elapsed_time)
                time.sleep(1)


if __name__ == "__main__":
    queue: Song_Queue = Song_Queue(FOLDER)
    player: Player = Player(queue)
    player.run()
