from aqt import mw
from aqt.qt import QAction
from .view import get_card_input_dialog, show_info, show_warning
from .german_card import GermanCard, ensure_german_model_exists, german_card_to_anki_note

def generate_card():
    result = get_card_input_dialog(mw)
    if not result:
        return

    card = GermanCard.create_from_user_input(result, mw)
    if not card.is_valid():
        show_warning("Invalid card data.")
        return

    model = ensure_german_model_exists(mw)
    note = german_card_to_anki_note(card, mw, model)
    mw.col.add_note(note, result.selected_deck_id)
    mw.col.save()
    if card.audio_filename:
        show_info(f"German card created with audio: {card.word}")
    else:
        show_info(f"German card created: {card.word}")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 