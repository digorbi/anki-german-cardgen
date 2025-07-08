import os
from typing import Any

from core.audio_card import AudioCard


class AnkiService:
    def __init__(self, mw: Any) -> None:
        self.mw = mw

    def _ensure_model_exists(self, card: AudioCard) -> Any:
        """
        Ensure the model for the given AudioCard exists in Anki, creating it if
        necessary.
        Returns the model.
        """
        model_name = card.get_model_name()
        model = self.mw.col.models.by_name(model_name)
        if model:
            return model
        # Create new model
        model = self.mw.col.models.new(model_name)
        fields_map = card.get_fields()
        for field in fields_map.keys():
            self.mw.col.models.add_field(model, self.mw.col.models.new_field(field))
        template_data = card.get_template()
        template = self.mw.col.models.new_template(card.get_template_name())
        template['qfmt'] = template_data.get('qfmt', '')
        template['afmt'] = template_data.get('afmt', '')
        self.mw.col.models.add_template(model, template)
        self.mw.col.models.add(model)
        return model

    def _save_card_audio_to_media(self, card: AudioCard) -> None:
        """
        Save the audio data from the AudioCard to Anki's media directory,
        overwriting if it exists.
        Does nothing if there is no audio data or filename.
        """
        audio_data = card.get_audio_data()
        filename = card.get_audio_filename()
        if audio_data is None or not filename:
            return
        media_dir = self.mw.col.media.dir()
        destination = os.path.join(media_dir, filename)
        try:
            with open(destination, "wb") as fh:
                fh.write(audio_data)
        except Exception:
            pass

    def save_card(self, card: AudioCard, deck_id: Any) -> Any:
        """
        Save an AudioCard to Anki in the specified deck.
        """
        model = self._ensure_model_exists(card)
        note = self.mw.col.new_note(model)
        fields_map = card.get_fields()
        for i, value in enumerate(fields_map.values()):
            note.fields[i] = value
        self.mw.col.add_note(note, deck_id)
        self.mw.col.save()
        self._save_card_audio_to_media(card)
        return note
