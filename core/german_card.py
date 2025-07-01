from .audio_card import AudioCard
import re

class GermanCard(AudioCard):
    def __init__(
        self,
        term: str,
        context: str,
        audio_path: str
    ):
        self._id = self._gen_id(term)
        self.term = term
        self.context = context
        self.audio_path = audio_path
        self._audio_filename = self._gen_audio_filename(audio_path)
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

    def _gen_audio_filename(self, audio_path: str) -> str:
        if audio_path:
            import os
            filename = os.path.basename(audio_path)
            audio_filename = f"[sound:{filename}]"
        else:
            audio_filename = ""
        return audio_filename

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

    def get_audio_path(self) -> str:
        return self.audio_path

    def to_fields_list(self) -> list:
        return [
            self._id,
            self.term,
            self.sentence,
            self._audio_filename,
            self.term_translation,
            self.sentence_translation,
            self.context
        ]

    @classmethod
    def create_from_user_input(cls, term, audio_path):
        card = cls(term, "Example context for {term}", audio_path)
        card.sentence = "Example sentence with {term}"
        card.term_translation = "Translation of {term}"
        card.sentence_translation = "Translation of example sentence with {term}"
        return card