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

    @classmethod
    def create_from_user_input(cls, result, mw):
        """
        Create a GermanCard from user input, handling business logic and audio file copying.
        """
        word = result.word
        audio_path = result.audio_path

        # Business logic for generating example sentence and translations
        example_sentence = f"Example sentence with {word}"
        word_translation = f"Translation of {word}"
        sentence_translation = "Translation of example sentence"

        # Handle audio file
        audio_filename = ""
        if audio_path:
            audio_filename = cls.copy_audio_to_media(audio_path, mw)

        return cls(
            word=word,
            example_sentence=example_sentence,
            audio_filename=audio_filename or "",
            word_translation=word_translation,
            sentence_translation=sentence_translation,
            note=""
        )

    @staticmethod
    def copy_audio_to_media(audio_path, mw):
        import os
        import shutil
        try:
            if not audio_path or not os.path.exists(audio_path):
                return None
            original_filename = os.path.basename(audio_path)
            media_dir = mw.col.media.dir()
            filename = original_filename
            counter = 1
            while os.path.exists(os.path.join(media_dir, filename)):
                name, ext = os.path.splitext(original_filename)
                filename = f"{name}_{counter}{ext}"
                counter += 1
            destination = os.path.join(media_dir, filename)
            shutil.copy2(audio_path, destination)
            return filename
        except Exception as e:
            # Optionally, handle error reporting here or in the controller
            return None

def ensure_german_model_exists(mw):
    """
    Ensure the GermanCardModel exists in Anki, creating it if necessary.
    """
    model_name = "GermanCardModel"
    existing = mw.col.models.by_name(model_name)
    if existing:
        return existing
    model = mw.col.models.new(model_name)
    for field in ["id", "de_word", "de_sentence", "de_audio", "word_translation", "sentence_translation", "note"]:
        mw.col.models.add_field(model, mw.col.models.new_field(field))
    template = mw.col.models.new_template("German → English")
    template['qfmt'] = """
<div class=\"german-word\">{{de_word}}</div>
<div class=\"german-sentence\">{{de_sentence}}</div>
{{de_audio}}
"""
    template['afmt'] = """
<div class=\"german-word\">{{de_word}}</div>
<div class=\"word-translation\">{{word_translation}}</div>
<div class=\"german-sentence\">{{de_sentence}}</div>
<div class=\"sentence-translation\">{{sentence_translation}}</div>
{{de_audio}}
<div class=\"notes\">{{note}}</div>
"""
    mw.col.models.add_template(model, template)
    mw.col.models.add(model)
    return model

def german_card_to_anki_note(card: GermanCard, mw, model):
    """
    Convert a GermanCard instance to an Anki note.
    """
    note = mw.col.new_note(model)
    fields = card.to_fields_list()
    for i, value in enumerate(fields):
        note.fields[i] = value
    return note 