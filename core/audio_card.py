"""Protocol defining the minimal interface for audio-based cards."""

from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class AudioCard(Protocol):
    def get_model_name(self) -> str:
        ...

    def get_template_name(self) -> str:
        ...

    def get_fields(self) -> dict:
        """Return mapping of field names to values."""
        ...

    def get_template(self) -> dict:
        """Return mapping with 'qfmt' and 'afmt' template strings."""
        ...

    def get_audio_data(self) -> Optional[bytes]:
        ...

    def get_audio_filename(self) -> str:
        ...
