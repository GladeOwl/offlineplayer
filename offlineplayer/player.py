import time
import simpleaudio
from pydub import AudioSegment
from rich.progress import Progress


SONGPATH: str = "D:\Music\Backup\Lauren Aquilina - King (Lyrics).mp3"


class Player:
    def __init__(self, song_file: str) -> None:
        self.song: AudioSegment = AudioSegment.from_mp3(song_file)
        self.song_name: str = song_file.split("\\")[-1]

        self.play()
        self.progress()

    def play(self) -> None:
        self.play_obj: simpleaudio.PlayObject = simpleaudio.play_buffer(
            audio_data=self.song.raw_data,
            num_channels=self.song.channels,
            bytes_per_sample=self.song.sample_width,
            sample_rate=self.song.frame_rate,
        )

    def progress(self) -> None:
        self.start_time: float = time.time()

        with Progress() as progress:
            task = progress.add_task(
                f"[green] {self.song_name}", total=self.song.duration_seconds
            )
            while self.play_obj.is_playing():
                elapsed_time = time.time() - self.start_time
                progress.update(task, completed=elapsed_time)
                time.sleep(1)


if __name__ == "__main__":
    player: Player = Player(SONGPATH)
