import os
from typing import Any, Tuple

from core.audio_card import AudioCard


class AnkiService:
    def __init__(self, mw: Any, model_name: str, template_name: str) -> None:
        self.mw = mw
        self.model_name = model_name
        self.template_name = template_name

    def _ensure_model_exists(self, card: AudioCard) -> Any:
        """
        Ensure the model for the given AudioCard exists in Anki, creating it if
        necessary.
        Returns the model.
        """
        model = self.mw.col.models.by_name(self.model_name)
        if model:
            return model
        # Create new model
        model = self.mw.col.models.new(self.model_name)
        fields_map = card.get_fields()
        for field in fields_map.keys():
            self.mw.col.models.add_field(model, self.mw.col.models.new_field(field))
        template_data = card.get_template()
        template = self.mw.col.models.new_template(self.template_name)
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

    def _delete_duplicated_cards(self, card_id: Tuple[str, str]) -> int:
        field_name, field_value = card_id
        note_ids = self.mw.col.find_notes(f'note:"{self.model_name}" {field_name}:"{field_value}"')
        if note_ids:
            self.mw.col.remove_notes(note_ids)
            self.mw.col.save()

        return len(note_ids)

    def save_card(self, card: AudioCard, deck_id: Any) -> int:
        """
        Save an AudioCard to Anki in the specified deck.
        Replaces all cards with the same card ID and returns the number of removed.
        """
        model = self._ensure_model_exists(card)
        removed = self._delete_duplicated_cards(card.get_unique_id())

        note = self.mw.col.new_note(model)
        fields_map = card.get_fields()
        for i, value in enumerate(fields_map.values()):
            note.fields[i] = value
        self.mw.col.add_note(note, deck_id)
        self.mw.col.save()
        self._save_card_audio_to_media(card)
        return removed
