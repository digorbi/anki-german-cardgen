from aqt import mw
from aqt.qt import QAction
from .view import get_card_input_dialog, show_info, show_warning
from .german_card import GermanCard
from .anki_service import AnkiService

def generate_card():
    result = get_card_input_dialog(mw)
    if not result:
        return

    print(f"DEBUG: User input - word: '{result.word}', audio_path: '{result.audio_path}'")
    
    card = GermanCard.create_from_user_input(result)
    if not card.is_valid():
        show_warning("Invalid card data.")
        return

    print(f"DEBUG: Card created - audio_path: '{card.audio_path}', audio_filename: '{card.audio_filename}'")

    # Use AnkiService to handle card creation and audio copying
    anki_service = AnkiService(mw)
    try:
        note = anki_service.save_card(card, result.selected_deck_id)
        show_info(f"German card created: {card.word}")
    except Exception as e:
        show_warning(f"Failed to create card: {str(e)}")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 