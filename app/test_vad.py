import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import numpy as np
import torch

from audio.frame import AudioFrame
from core.event_bus import EventBus
from core.events import SpeechEnded, SpeechStarted
from vad.detector import VoiceActivityDetector


class VoiceActivityDetectorTests(unittest.TestCase):
    def test_model_runs_once_per_frame_and_publishes_boundaries(self):
        model = Mock()
        model.side_effect = [torch.tensor(0.9)] + [torch.tensor(0.1)] * 20
        events = []
        bus = EventBus()
        bus.subscribe(SpeechStarted, events.append)
        bus.subscribe(SpeechEnded, events.append)

        with patch("vad.detector.load_silero_vad", return_value=model):
            detector = VoiceActivityDetector(bus)

        for _ in range(20):
            detector.process(
                AudioFrame(
                    data=np.ones((512, 1), dtype=np.int16),
                    sample_rate=16000,
                    channels=1,
                    timestamp=datetime.now(),
                )
            )

        self.assertEqual(model.call_count, 20)
        self.assertEqual([type(event) for event in events], [SpeechStarted, SpeechEnded])


if __name__ == "__main__":
    unittest.main()
