from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    BLOCK_SIZE: int = 512
    DTYPE: str = "int16"


@dataclass(frozen=True)
class WhisperConfig:
    MODEL_NAME: str = "small"
    DEVICE: str = "cpu"
    COMPUTE_TYPE: str = "int8"


@dataclass(frozen=True)
class AppConfig:
    APP_NAME: str = "Jarvis"
    VERSION: str = "1.0.0"


audio = AudioConfig()
whisper = WhisperConfig()
app = AppConfig()