import sys
import os
# Add the addon directory to Python path so core package can be found
addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from aqt import mw
from aqt.qt import QAction
from .view import get_card_input_dialog, show_info, show_warning
from core.german_card import GermanCard
from .anki_service import AnkiService

def generate_card():
    result = get_card_input_dialog(mw)
    if not result:
        return
   
    # TODO: create vocab provider and pass it to the card.

    card = GermanCard.create_from_user_input(result.term, result.audio_path)
    if not card.is_valid():
        show_warning("Invalid card data.")
        return
    
    anki_service = AnkiService(mw)
    try:
        anki_service.save_card(card, result.selected_deck_id)
        show_info(f"German card created: {card.term}")
    except Exception as e:
        show_warning(f"Failed to create card: {str(e)}")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 