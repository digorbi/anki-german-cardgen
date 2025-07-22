from __future__ import annotations

import os
import re
from typing import Optional

from .audio_provider import AudioProvider
from .vocab_provider import VocabProvider


class GermanCard:
    _UMLAUTS = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss',
    }

    CARD_TEMPLATE_DEFAULT = "german_card_default"

    def __init__(
        self,
        term: str,
        context: str,
        template: str = CARD_TEMPLATE_DEFAULT,
    ):
        self._id = self._gen_id(term)
        self.term = term
        self.context = context
        self._audio_data: Optional[bytes] = None
        self._audio_filename = ""
        self.sentence = ""
        self.term_translation = ""
        self.sentence_translation = ""

        #Load templates
        templates_dir = os.path.join(
            os.path.dirname(__file__), "..", "templates", template
        )
        self._front_template = self._load_template(templates_dir, "front.html")
        self._back_template = self._load_template(templates_dir, "back.html")
        self._style_template = self._load_template(templates_dir, "style.css")

    @staticmethod
    def _load_template(directory: str, filename: str) -> str:
        path = os.path.join(directory, filename)
        with open(path, encoding="utf-8") as fh:
            return fh.read()

    def _gen_id(self, term: str) -> str:
        """Generate ID based on term value by converting to lowercase and
        replacing spaces with underscores"""
        # Convert to lowercase and replace spaces with underscores
        id_base = term.lower().replace(' ', '_')
        # Replace German umlauts with their ASCII equivalents
        for umlaut, replacement in self._UMLAUTS.items():
            id_base = id_base.replace(umlaut, replacement)
        # Remove any remaining special characters and keep only alphanumeric
        # and underscores
        return re.sub(r'[^a-z0-9_]', '', id_base)

    def get_unique_id(self) -> tuple[str, str]:
        return "id", self._id

    def is_valid(self) -> bool:
        return bool(self._id)

    def get_fields(self) -> dict[str, str]:
        if self._audio_filename:
            audio_field = f"[sound:{self._audio_filename}]"
        else:
            audio_field = ""
        return {
            "id": self._id,
            "term": self.term,
            "sentence": self.sentence,
            "sentence_audio": audio_field,
            "term_translation": self.term_translation,
            "sentence_translation": self.sentence_translation,
            "context": self.context,
        }

    def get_template(self) -> dict[str, str]:
        return {
            "qfmt": self._front_template,
            "afmt": self._back_template,
            "css": self._style_template,
        }

    def get_audio_data(self) -> Optional[bytes]:
        return self._audio_data

    def get_audio_filename(self) -> str:
        return self._audio_filename

    @classmethod
    def create_from_user_input(
        cls,
        term: str,
        context: str,
        vocab_provider: VocabProvider,
        audio_provider: AudioProvider,
    ) -> GermanCard:
        """Create a card using vocabulary data from ``vocab_provider``."""

        data = vocab_provider.get_vocab(term, context)
        card = cls(data.term, context)
        card.sentence = data.sentence
        card.term_translation = data.term_translation
        card.sentence_translation = data.sentence_translation

        card._audio_data = audio_provider.get_audio(card.sentence)
        card._audio_filename = audio_provider.get_file_name(card._id)

        return card

