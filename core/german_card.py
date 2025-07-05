from .audio_card import AudioCard
from .vocab_provider import VocabProvider
from .audio_provider import AudioProvider
import re
from typing import Optional

class GermanCard(AudioCard):
    def __init__(
        self,
        term: str,
        context: str,
    ):
        self._id = self._gen_id(term)
        self.term = term
        self.context = context
        self._audio_data = None
        self._audio_filename = ""
        self.sentence = ""
        self.term_translation = ""
        self.sentence_translation = ""

    def _gen_id(self, term: str):
        """Generate ID based on term value by converting to lowercase and replacing spaces with underscores"""
        # Convert to lowercase and replace spaces with underscores
        id_base = term.lower().replace(' ', '_')
        
        # Handle German umlauts and special characters
        umlaut_map = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'
        }
        
        # Replace umlauts and special characters
        for umlaut, replacement in umlaut_map.items():
            id_base = id_base.replace(umlaut, replacement)
        
        # Remove any remaining special characters and keep only alphanumeric and underscores
        return re.sub(r'[^a-z0-9_]', '', id_base)

    def is_valid(self):
        return bool(self._id)

    # AudioCard interface implementation
    def get_model_name(self) -> str:
        return "German Contextual Vocab"

    def get_model_fields_names(self) -> list:
        return ["id", "term", "sentence", "sentence_audio", "term_translation", "sentence_translation", "context"]

    def get_template_name(self) -> str:
        return "Contextual Audio Card"

    def get_qfmt_template(self) -> str:
        return """
<div class="term">{{term}}</div>
<div class="sentence">{{sentence}}</div>
{{sentence_audio}}
"""

    def get_afmt_template(self) -> str:
        return """
<div class="term">{{term}}</div>
<div class="term-translation">{{term_translation}}</div>
<div class="sentence">{{sentence}}</div>
<div class="sentence-translation">{{sentence_translation}}</div>
{{sentence_audio}}
<div class="context">{{context}}</div>
"""

    def to_fields_list(self) -> list:
        if self._audio_filename:
            audio_field = f"[sound:{self._audio_filename}]"
        else:
            audio_field = ""

        return [
            self._id,
            self.term,
            self.sentence,
            audio_field,
            self.term_translation,
            self.sentence_translation,
            self.context
        ]

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
        audio_provider: Optional[AudioProvider] = None,
    ):
        """Create a card using vocabulary data from ``vocab_provider``."""

        data = vocab_provider.get_vocab(term, context)
        card = cls(data.term, context)
        card.sentence = data.sentence
        card.term_translation = data.term_translation
        card.sentence_translation = data.sentence_translation

        if audio_provider is None:
            card._audio_data = None
        else:
            card._audio_data = audio_provider.get_audio(card.sentence)
            card._audio_filename = audio_provider.get_file_name(card._id)

        return card

