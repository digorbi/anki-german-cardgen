from .audio_card import AudioCard
import re

class GermanCard(AudioCard):
    def __init__(
        self,
        word: str,
        example_sentence: str,
        audio_filename: str = "",
        word_translation: str = "",
        sentence_translation: str = "",
        note: str = "",
        audio_path: str = ""
    ):
        self._id = self._gen_id(word)
        self.word = word
        self.example_sentence = example_sentence
        self.audio_filename = audio_filename
        self.word_translation = word_translation
        self.sentence_translation = sentence_translation
        self.note = note
        self.audio_path = audio_path

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
        return "GermanCardModel"

    def get_model_fields_names(self) -> list:
        return ["id", "de_word", "de_sentence", "de_audio", "word_translation", "sentence_translation", "note"]

    def get_template_name(self) -> str:
        return "German → English"

    def get_qfmt_template(self) -> str:
        return """
<div class="german-word">{{de_word}}</div>
<div class="german-sentence">{{de_sentence}}</div>
{{de_audio}}
"""

    def get_afmt_template(self) -> str:
        return """
<div class="german-word">{{de_word}}</div>
<div class="word-translation">{{word_translation}}</div>
<div class="german-sentence">{{de_sentence}}</div>
<div class="sentence-translation">{{sentence_translation}}</div>
{{de_audio}}
<div class="notes">{{note}}</div>
"""

    def get_audio_path(self) -> str:
        return self.audio_path

    def to_fields_list(self) -> list:
        return [
            self._id,
            self.word,
            self.example_sentence,
            self.audio_filename,
            self.word_translation,
            self.sentence_translation,
            self.note
        ]

    @classmethod
    def create_from_user_input(cls, result):
        """
        Create a GermanCard from user input, handling business logic.
        Audio file copying is now handled by AnkiService through the AudioCard interface.
        """
        word = result.word
        audio_path = result.audio_path

        # Business logic for generating example sentence and translations
        example_sentence = f"Example sentence with {word}"
        word_translation = f"Translation of {word}"
        sentence_translation = "Translation of example sentence"

        # Extract filename from audio path if provided
        audio_filename = ""
        if audio_path:
            import os
            filename = os.path.basename(audio_path)
            audio_filename = f"[sound:{filename}]"

        return cls(
            word=word,
            example_sentence=example_sentence,
            audio_filename=audio_filename,
            word_translation=word_translation,
            sentence_translation=sentence_translation,
            note="",
            audio_path=audio_path or ""
        ) 