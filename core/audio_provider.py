"""Audio provider protocol used for supplying sound data."""

from typing import Protocol, runtime_checkable

@runtime_checkable
class AudioProvider(Protocol):
    """Protocol describing an object that can supply audio data."""

    def get_audio(self, text: str) -> bytes:
        """Return audio bytes for the given text."""
        ...

    def get_file_name(self, base: str) -> str:
        """Return a unique audio filename for ``base``."""
        ...
