import numpy as np
import torch
from datetime import datetime

from silero_vad import load_silero_vad, VADIterator

from audio.frame import AudioFrame
from core.logger import get_logger
from core.events import SpeechStarted, SpeechEnded


logger = get_logger(__name__)


class _ProbabilityTrackingModel:
    def __init__(self, model):
        self.model = model
        self.probability = 0.0

    def reset_states(self):
        self.model.reset_states()
        self.probability = 0.0

    def __call__(self, audio: torch.Tensor, sample_rate: int) -> torch.Tensor:
        result = self.model(audio, sample_rate)
        self.probability = float(result.item())
        return result


class VoiceActivityDetector:
    """
    Streaming Voice Activity Detector using Silero VAD.

    Responsibilities:
    -----------------
    1. Receive AudioFrame objects.
    2. Run Silero VAD.
    3. Publish SpeechStarted and SpeechEnded events.
    4. Annotate the frame with speech information.
    """

    def __init__(self, event_bus):

        self.event_bus = event_bus

        self.sample_rate = 16000
        self.threshold = 0.5

        self.model = _ProbabilityTrackingModel(load_silero_vad())

        self.iterator = VADIterator(
            self.model,
            threshold=self.threshold,
            sampling_rate=self.sample_rate,
            min_silence_duration_ms=1000,
            speech_pad_ms=100,
        )

    def process(self, frame: AudioFrame):

        # Convert int16 -> float32
        audio = frame.data.astype(np.float32)

        audio /= 32768.0

        audio = np.squeeze(audio)

        audio_tensor = torch.from_numpy(audio)

        # Get speech boundary events
        with torch.no_grad():
            event = self.iterator(
                audio_tensor,
                return_seconds=True,
            )

        probability = self.model.probability

        # Store metadata in frame
        frame.speech_probability = probability
        frame.is_speech = probability >= self.threshold

        logger.debug(
            "Speech=%s | Probability=%.3f",
            frame.is_speech,
            probability,
        )

        # No speech transition
        if event is None:
            return

        # Speech Started
        if "start" in event:

            logger.info(
                "Speech Started (%.2f sec)",
                event["start"],
            )

            self.event_bus.publish(
                SpeechStarted(
                    timestamp=datetime.now()
                )
            )

        # Speech Ended
        if "end" in event:

            logger.info(
                "Speech Ended (%.2f sec)",
                event["end"],
            )

            self.event_bus.publish(
                SpeechEnded(
                    timestamp=datetime.now()
                )
            )