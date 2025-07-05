import sys
import os
# Add the addon directory to Python path so core package can be found
addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from aqt import mw
from aqt.qt import QAction
from .view import (
    get_card_input_dialog,
    get_api_settings_dialog,
    show_info,
    show_warning,
)
from core.german_card import GermanCard
from core.openai_vocab_provider import OpenaiVocabProvider
from core.gtts_audio_provider import GttsAudioProvider
from .anki_service import AnkiService


def ensure_settings():
    """Return API key and target language from config, prompting the user if needed."""
    config = mw.addonManager.getConfig(__name__) or {}
    api_key = config.get("openai_api_key", "")
    target_language = config.get("target_language", "")
    if not api_key or not target_language:
        result = get_api_settings_dialog(mw, api_key, target_language or "English")
        if not result:
            return None, None
        api_key, target_language = result
        config["openai_api_key"] = api_key
        config["target_language"] = target_language
        mw.addonManager.writeConfig(__name__, config)
    return api_key, target_language

def generate_card():
    api_key, target_language = ensure_settings()
    if not api_key or not target_language:
        show_warning("OpenAI configuration required to generate card.")
        return    
    
    result = get_card_input_dialog(mw)
    if not result:
        return

    vocab_provider = OpenaiVocabProvider(api_key, target_language)
    audio_provider = GttsAudioProvider("de")

    card = GermanCard.create_from_user_input(
        result.term, "", vocab_provider, audio_provider
    )
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
