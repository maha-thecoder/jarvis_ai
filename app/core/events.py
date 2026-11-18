from dataclasses import dataclass
from datetime import datetime


@dataclass
class SpeechStarted:
    timestamp: datetime


@dataclass
class SpeechEnded:
    timestamp: datetime


@dataclass
class TranscriptReady:
    text: str
    audio_path: str