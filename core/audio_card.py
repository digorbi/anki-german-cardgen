from abc import ABC, abstractmethod

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
    def get_audio_path(self) -> str:
        pass

    @abstractmethod
    def to_fields_list(self) -> list:
        pass 