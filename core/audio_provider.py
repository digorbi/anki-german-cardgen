from abc import ABC, abstractmethod

class AudioProvider(ABC):
    """Abstract base class for audio providers."""

    @abstractmethod
    def get_audio(self, text: str) -> bytes:
        """Return audio bytes for the given text."""
        raise NotImplementedError

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider short provider name that can be used in the filename as a prefix."""
        raise NotImplementedError


