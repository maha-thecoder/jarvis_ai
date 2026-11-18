from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class AudioFrame:
    """
    Represents one chunk of audio flowing through the pipeline.
    Each processor may enrich this object with additional metadata.
    """

    data: np.ndarray
    sample_rate: int
    channels: int
    timestamp: datetime

    # Filled by downstream processors
    speech_probability: float | None = None
    is_speech: bool | None = None