from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from pathlib import Path
from shutil import copyfile
from uuid import uuid4

from analyser.executor import ToolExecutor

from memory.session_manager import SessionManager

from audio.frame import AudioFrame

from core.logger import get_logger
from core.events import SpeechStarted, SpeechEnded

from wakeword.detector import WakeWordDetector

from recorder.recorder import AudioRecorder

from speech.whisper_service import WhisperService

from intent.router import IntentRouter


logger = get_logger(__name__)


class SpeechService:


    def __init__(self):

        # Audio recording
        self.recorder = AudioRecorder()


        # Speech to text
        self.whisper = WhisperService()


        # Wake word detection
        self.wakeword = WakeWordDetector()


        # Intent understanding
        self.intent_router = IntentRouter()


        # Action analyser
        self.tool_executor = ToolExecutor()


        # Memory/session
        self.session = SessionManager()



        # Background transcription
        self._transcription_executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="jarvis-transcription",
        )



    # ==================================================
    # Speech Started
    # ==================================================

    def on_speech_started(
        self,
        event: SpeechStarted
    ) -> None:


        logger.info(
            "Speech Started at %s",
            event.timestamp
        )


        self.recorder.start()



    # ==================================================
    # Receive Audio Frames
    # ==================================================

    def on_audio_frame(
        self,
        frame: AudioFrame
    ) -> None:


        if not self.recorder.recording:

            return


        self.recorder.add_frame(frame)



    # ==================================================
    # Speech Ended
    # ==================================================

    def on_speech_ended(
        self,
        event: SpeechEnded
    ) -> None:


        logger.info(
            "Speech Ended at %s",
            event.timestamp
        )


        wav = self.recorder.stop()


        if not wav:

            return



        audio_path = Path(wav)


        # Create temporary copy for whisper

        transcription_path = audio_path.with_name(
            f"{audio_path.stem}_{uuid4().hex}{audio_path.suffix}"
        )



        copyfile(
            audio_path,
            transcription_path
        )



        logger.info(
            "Saved -> %s",
            wav
        )


        logger.info(
            "Queued transcription..."
        )



        future = self._transcription_executor.submit(
            self.whisper.transcribe,
            str(transcription_path)
        )



        future.add_done_callback(
            lambda completed:
            self._on_transcription_complete(
                completed,
                transcription_path
            )
        )



    # ==================================================
    # Whisper Result
    # ==================================================

    def _on_transcription_complete(
        self,
        future: Future[str],
        audio_path: Path
    ):


        try:

            text = future.result()



        except CancelledError:


            logger.info(
                "Transcription cancelled"
            )


            return



        except Exception:


            logger.exception(
                "Whisper transcription failed"
            )


            return



        else:


            logger.info(
                "You said: %s",
                text
            )



            # Save conversation memory

            self.session.add_text(
                text
            )



            # Wake word check

            if not self.wakeword.detect(text):


                logger.info(
                    "Wake word not detected"
                )


                return



            logger.info(
                "Wake word accepted"
            )



            # Intent classification

            intent = self.intent_router.classify(
                text
            )



            logger.info(
                "Detected Intent: %s",
                intent.name
            )


            logger.info(
                "Confidence: %.2f",
                intent.confidence
            )



            if intent.name == "UNKNOWN":


                logger.info(
                    "Unknown command"
                )


                return



            if intent.confidence < 0.50:


                logger.info(
                    "Low confidence intent ignored"
                )


                return



            # Send to analyser

            self.tool_executor.execute(
                intent
            )



        finally:


            try:

                audio_path.unlink(
                    missing_ok=True
                )


            except OSError:


                logger.exception(
                    "Failed deleting temporary audio"
                )



    # ==================================================
    # Shutdown
    # ==================================================

    def close(self):


        logger.info(
            "Closing Speech Service..."
        )



        self._transcription_executor.shutdown(
            wait=True
        )



        self.session.save_session()



        self.session.cleanup_recordings()



        logger.info(
            "Speech Service closed"
        )