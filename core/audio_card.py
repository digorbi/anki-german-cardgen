"""Protocol defining the minimal interface for audio-based cards."""

from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class AudioCard(Protocol):
    def get_unique_id(self) -> tuple[str, str]:
        """Return a unique identifier for the card.
        Represented as a tuple of a field name and value."""
        ...

    def get_fields(self) -> dict[str, str]:
        """Return mapping of field names to values."""
        ...

    def get_template(self) -> dict[str, str]:
        """Return mapping with 'qfmt' and 'afmt' template strings."""
        ...

    def get_audio_data(self) -> Optional[bytes]:
        ...

    def get_audio_filename(self) -> str:
        ...
