from dataclasses import dataclass


@dataclass
class IntentResult:

    name: str

    confidence: float

    text: str