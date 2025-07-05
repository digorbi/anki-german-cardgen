from abc import ABC, abstractmethod

class AudioProvider(ABC):
    """Abstract base class for audio providers."""

    @abstractmethod
    def get_audio(self, text: str) -> bytes:
        """Return audio bytes for the given text."""
        raise NotImplementedError

    @abstractmethod
    def get_file_name(self, base: str) -> str:
        """Returns the filename with the provider identifier and respected file format. Uses the base argument to ensure filename uniqueness."""
        raise NotImplementedError
