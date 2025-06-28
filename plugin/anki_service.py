import os
import shutil
from core.audio_card import AudioCard

class AnkiService:
    def __init__(self, mw):
        self.mw = mw

    def _ensure_model_exists(self, card: AudioCard):
        """
        Ensure the model for the given AudioCard exists in Anki, creating it if necessary.
        Returns the model.
        """
        model_name = card.get_model_name()
        model = self.mw.col.models.by_name(model_name)
        if model:
            return model
        # Create new model
        model = self.mw.col.models.new(model_name)
        fields_names = card.get_model_fields_names()
        if not fields_names or not hasattr(fields_names, '__iter__'):
            raise ValueError("get_model_fields_names() must return an iterable of field names")
        for field in fields_names:
            self.mw.col.models.add_field(model, self.mw.col.models.new_field(field))
        template = self.mw.col.models.new_template(card.get_template_name())
        template['qfmt'] = card.get_qfmt_template()
        template['afmt'] = card.get_afmt_template()
        self.mw.col.models.add_template(model, template)
        self.mw.col.models.add(model)
        return model

    def _copy_audio_to_media(self, card: AudioCard):
        """
        Copy the audio file to Anki's media directory, overwriting if it exists.
        Returns the filename used in the media directory, or None if no audio or copy failed.
        """
        audio_path = card.get_audio_path()
        if not audio_path or not os.path.exists(audio_path):
            return None
        filename = os.path.basename(audio_path)
        media_dir = self.mw.col.media.dir()
        destination = os.path.join(media_dir, filename)
        try:
            shutil.copy2(audio_path, destination)
            return filename
        except Exception:
            return None

    def save_card(self, card: AudioCard, deck_id):
        """
        Save a AudioCard to Anki in the specified deck.
        """
        model = self._ensure_model_exists(card)
        note = self.mw.col.new_note(model)
        fields = card.to_fields_list()
        if not isinstance(fields, list):
            raise ValueError("to_fields_list() must return a list")
        for i, value in enumerate(fields):
            note.fields[i] = value
        self.mw.col.add_note(note, deck_id)
        self.mw.col.save()
        self._copy_audio_to_media(card)
        return note 