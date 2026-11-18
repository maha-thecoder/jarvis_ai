from collections import deque
import numpy as np


class AudioBuffer:

    def __init__(self, max_frames: int = 10):
        self.frames = deque(maxlen=max_frames)

    def add(self, frame):
        self.frames.append(frame.data.copy())

    def ready(self) -> bool:
        return len(self.frames) == self.frames.maxlen

    def get_audio(self) -> np.ndarray:
        return np.concatenate(self.frames, axis=0)