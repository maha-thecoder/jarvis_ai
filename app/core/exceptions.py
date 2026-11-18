class JarvisError(Exception):
    """Base exception for Jarvis."""


class AudioError(JarvisError):
    """Audio related exception."""


class WhisperError(JarvisError):
    """Speech recognition exception."""


class WakeWordError(JarvisError):
    """Wake word exception."""