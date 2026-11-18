import queue
from datetime import datetime

import sounddevice as sd

from audio.frame import AudioFrame
from core.logger import get_logger

logger = get_logger(__name__)


class Microphone:
    """
    Captures audio from the microphone and pushes AudioFrames
    into a queue.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        block_size: int = 512,
        dtype: str = "int16",
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.dtype = dtype

        self.audio_queue = queue.Queue()
        self.stream = None

    def _callback(self, indata, _frames, _time, status):
        del _frames, _time

        if status:
            logger.warning(status)

        frame = AudioFrame(
            data=indata.copy(),
            sample_rate=self.sample_rate,
            channels=self.channels,
            timestamp=datetime.now(),
        )

        self.audio_queue.put(frame)

    def start(self):
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.block_size,
            callback=self._callback,
        )

        self.stream.start()

        logger.info("Microphone started")

    def stop(self):
        stream = self.stream
        self.stream = None

        if stream is not None:
            try:
                stream.stop()
            finally:
                stream.close()

        logger.info("Microphone stopped")

    def read(self):
        return self.audio_queue.get()