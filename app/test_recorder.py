import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf

from audio.frame import AudioFrame
from recorder.recorder import AudioRecorder


class AudioRecorderTests(unittest.TestCase):
    def test_records_frames_to_wav_and_resets_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            recorder = AudioRecorder(output_dir=temp_dir)
            frame = AudioFrame(
                data=np.ones((512, 1), dtype=np.int16),
                sample_rate=16000,
                channels=1,
                timestamp=datetime.now(),
            )

            recorder.start()
            recorder.add_frame(frame)
            wav_path = recorder.stop()

            self.assertEqual(wav_path, str(Path(temp_dir) / "temp.wav"))
            self.assertFalse(recorder.recording)
            audio, sample_rate = sf.read(wav_path)
            self.assertEqual(sample_rate, 16000)
            self.assertEqual(audio.shape, (512,))

    def test_empty_recording_returns_none(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            recorder = AudioRecorder(output_dir=temp_dir)
            recorder.start()

            self.assertIsNone(recorder.stop())
            self.assertFalse(recorder.recording)


if __name__ == "__main__":
    unittest.main()
