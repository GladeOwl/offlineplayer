import os


class Song_Queue:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.queue: list = os.listdir(self.path)
        self.number: int = 0
        self.current_track: str = None

    def next_track(self) -> str:
        self.current_track = self.queue[self.number]
        self.number += 1
        return self.current_track
