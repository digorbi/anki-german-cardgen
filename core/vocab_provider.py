"""Vocabulary provider abstractions and OpenAI implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class VocabItem:
    """Simple container for vocabulary information."""

    term: str = ""
    term_translation: str = ""
    sentence: str = ""
    sentence_translation: str = ""


class VocabProvider(ABC):
    """Abstract base class for vocabulary providers."""

    @abstractmethod
    def get_vocab(self, term: str, context: str = "") -> VocabItem:
        """Return :class:`VocabItem` for the given term."""
        raise NotImplementedError


