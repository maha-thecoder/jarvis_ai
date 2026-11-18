from audio.microphone import Microphone
from speech.frame_processor import FrameProcessor
from speech.speech_service import SpeechService

from vad.detector import VoiceActivityDetector

from core.event_bus import EventBus
from core.events import SpeechStarted, SpeechEnded


event_bus = EventBus()


speech_service = SpeechService()


event_bus.subscribe(
    SpeechStarted,
    speech_service.on_speech_started
)


event_bus.subscribe(
    SpeechEnded,
    speech_service.on_speech_ended
)


mic = Microphone()


processor = FrameProcessor()


vad = VoiceActivityDetector(
    event_bus
)


processor.add_processor(vad)



try:

    mic.start()


    while True:


        frame = mic.read()


        # record first
        speech_service.on_audio_frame(frame)


        # analyse speech
        processor.process(frame)



except KeyboardInterrupt:

    pass


finally:

    mic.stop()

    speech_service.close()