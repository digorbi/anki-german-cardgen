"""gTTS-based implementation of the :class:`AudioProvider` interface."""

from __future__ import annotations

import io
import os
from typing import Any, Optional

from .audio_provider import AudioProvider


class GttsAudioProvider(AudioProvider):
    """Retrieve audio data using the gTTS library."""

    def __init__(self, lang: str = "de", *, gtts_factory: Optional[Any] = None) -> None:
        if gtts_factory is None:
            # Try to import from bundled vendor directory first
            # This mirrors the approach used for the OpenAI provider and allows
            # the addon to work without requiring users to install dependencies.
            try:
                import sys

                addon_dir = os.path.dirname(os.path.dirname(__file__))
                vendor_dir = os.path.join(addon_dir, "vendor")

                if os.path.exists(vendor_dir) and vendor_dir not in sys.path:
                    sys.path.insert(0, vendor_dir)

                from gtts import gTTS  # type: ignore
                self._gtts_factory = gTTS
            except ImportError as exc:  # pragma: no cover - import error path
                raise ImportError(
                    "The 'gTTS' package is missing. Please ensure the addon was bundled correctly."
                ) from exc
        else:
            self._gtts_factory = gtts_factory

        self.lang = lang

    def get_audio(self, text: str) -> bytes:
        """Return MP3 audio bytes for the given text."""
        tts = self._gtts_factory(text=text, lang=self.lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()

    def get_file_name(self, base: str) -> str:
        """Return unique audio filename for the provided base id."""
        return f"{base}_gtts.mp3"
