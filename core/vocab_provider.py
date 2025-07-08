"""Vocabulary provider abstractions and OpenAI implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable



@dataclass
class VocabItem:
    """Simple container for vocabulary information."""

    term: str = ""
    term_translation: str = ""
    sentence: str = ""
    sentence_translation: str = ""



@runtime_checkable
class VocabProvider(Protocol):
    """Protocol describing a provider capable of returning vocabulary info."""

    def get_vocab(self, term: str, context: str = "") -> VocabItem:
        """Return :class:`VocabItem` for the given term."""
        ...


