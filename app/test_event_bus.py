import contextlib
import io
import tempfile
import threading
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from audio.frame import AudioFrame
from core.event_bus import EventBus
from core.events import SpeechEnded, SpeechStarted
from recorder.recorder import AudioRecorder
from speech.speech_service import SpeechService


class EventBusTests(unittest.TestCase):
    def test_publish_calls_handlers_for_matching_event_type(self):
        bus = EventBus()
        handler = Mock()
        event = SpeechStarted(datetime.now())
        bus.subscribe(SpeechStarted, handler)

        bus.publish(event)

        handler.assert_called_once_with(event)


class SpeechPipelineTests(unittest.TestCase):
    def test_speech_events_record_transcribe_and_reset_recorder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            recorder = AudioRecorder(output_dir=temp_dir)
            whisper = Mock()
            transcription_started = threading.Event()
            release_transcription = threading.Event()
            transcription_complete = threading.Event()
            transcribed_paths = []

            def transcribe(path):
                if not Path(path).is_file():
                    raise AssertionError("Transcription snapshot does not exist")
                transcribed_paths.append(path)
                transcription_started.set()
                if not release_transcription.wait(timeout=5):
                    raise TimeoutError("Test did not release the transcription worker")
                if len(transcribed_paths) == 2:
                    transcription_complete.set()
                return "hello jarvis"

            whisper.transcribe.side_effect = transcribe
            with (
                patch("speech.speech_service.AudioRecorder", return_value=recorder),
                patch("speech.speech_service.WhisperService", return_value=whisper),
            ):
                service = SpeechService()
            self.addCleanup(service.close)
            self.addCleanup(release_transcription.set)

            bus = EventBus()
            bus.subscribe(SpeechStarted, service.on_speech_started)
            bus.subscribe(SpeechEnded, service.on_speech_ended)
            frame = AudioFrame(
                data=np.ones((512, 1), dtype=np.int16),
                sample_rate=16000,
                channels=1,
                timestamp=datetime.now(),
            )

            bus.publish(SpeechStarted(datetime.now()))
            service.on_audio_frame(frame)
            with contextlib.redirect_stdout(io.StringIO()):
                bus.publish(SpeechEnded(datetime.now()))

            wav_path = Path(temp_dir) / "temp.wav"
            self.assertTrue(wav_path.is_file())
            self.assertFalse(recorder.recording)
            self.assertTrue(transcription_started.wait(timeout=5))

            bus.publish(SpeechStarted(datetime.now()))
            service.on_audio_frame(frame)
            with contextlib.redirect_stdout(io.StringIO()):
                bus.publish(SpeechEnded(datetime.now()))

            release_transcription.set()
            self.assertTrue(transcription_complete.wait(timeout=5))
            self.assertEqual(whisper.transcribe.call_count, 2)
            self.assertNotEqual(transcribed_paths[0], transcribed_paths[1])
            self.assertFalse(recorder.recording)

    def test_empty_segment_does_not_call_whisper(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            recorder = AudioRecorder(output_dir=temp_dir)
            whisper = Mock()
            with (
                patch("speech.speech_service.AudioRecorder", return_value=recorder),
                patch("speech.speech_service.WhisperService", return_value=whisper),
            ):
                service = SpeechService()
            self.addCleanup(service.close)

            service.on_speech_started(SpeechStarted(datetime.now()))
            service.on_speech_ended(SpeechEnded(datetime.now()))

            whisper.transcribe.assert_not_called()
            self.assertFalse(recorder.recording)


if __name__ == "__main__":
    unittest.main()
