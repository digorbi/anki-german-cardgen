from abc import ABC, abstractmethod
from typing import Optional

class AudioCard(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_model_fields_names(self) -> list:
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_qfmt_template(self) -> str:
        pass

    @abstractmethod
    def get_afmt_template(self) -> str:
        pass

    @abstractmethod
    def to_fields_list(self) -> list:
        pass

    @abstractmethod
    def get_audio_data(self) -> Optional[bytes]:
        pass

    @abstractmethod
    def get_audio_filename(self) -> str:
        pass
