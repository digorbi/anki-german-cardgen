from abc import ABC, abstractmethod
from typing import Optional

class AudioCard(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_fields(self) -> dict:
        """Return mapping of field names to values."""
        pass

    @abstractmethod
    def get_template(self) -> dict:
        """Return mapping with 'qfmt' and 'afmt' template strings."""
        pass

    @abstractmethod
    def get_audio_data(self) -> Optional[bytes]:
        pass

    @abstractmethod
    def get_audio_filename(self) -> str:
        pass
