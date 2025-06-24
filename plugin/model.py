class GermanCard:
    def __init__(
        self,
        word: str,
        example_sentence: str,
        audio_filename: str = "",
        word_translation: str = "",
        sentence_translation: str = "",
        note: str = "",
        card_id: str = "1"
    ):
        self.card_id = card_id
        self.word = word
        self.example_sentence = example_sentence
        self.audio_filename = audio_filename
        self.word_translation = word_translation
        self.sentence_translation = sentence_translation
        self.note = note

    def is_valid(self):
        return bool(self.word)

    def format_audio_field(self):
        if self.audio_filename:
            return f"[sound:{self.audio_filename}]"
        return ""

    def to_fields_list(self):
        return [
            self.card_id,
            self.word,
            self.example_sentence,
            self.format_audio_field(),
            self.word_translation,
            self.sentence_translation,
            self.note
        ] 