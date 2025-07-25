# ruff: noqa: E402
import os
import sys
from typing import Optional

# Add the addon directory to Python path so core package can be found
addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from aqt import mw  # type: ignore
from aqt.qt import QAction  # type: ignore

from core.german_card import GermanCard
from core.gtts_audio_provider import GttsAudioProvider
from core.openai_vocab_provider import OpenaiVocabProvider

from .anki_service import AnkiService

MODEL_NAME = "German Contextual Vocab"
TEMPLATE_NAME = "Contextual Audio Card"
from .view import (
    CardPreviewResult,
    SettingsResult,
    get_card_input_dialog,
    get_settings_dialog,
    show_card_preview_dialog,
    show_info,
    show_warning,
)


def ensure_settings() -> Optional[SettingsResult]:
    """Return API key and target language from config, prompting the user if needed."""
    config = mw.addonManager.getConfig(__name__) or {}
    api_key = config.get("openai_api_key", "")
    target_language = config.get("target_language", "")
    if not api_key or not target_language:
        result = get_settings_dialog(mw, api_key, target_language or "English")
        if not result:
            return None

        config["openai_api_key"] = result.api_key
        config["target_language"] = result.target_language
        mw.addonManager.writeConfig(__name__, config)
    # If config is present, construct a SettingsResult
    return SettingsResult(api_key=api_key, target_language=target_language)

def generate_card() -> None:
    settings = ensure_settings()
    if not settings:
        show_warning("OpenAI configuration required to generate card.")
        return

    result = get_card_input_dialog(mw)
    if not result:
        return

    while True:  # Allow regeneration loop
        vocab_provider = OpenaiVocabProvider(settings.api_key, settings.target_language)
        audio_provider = GttsAudioProvider("de")

        card = GermanCard.create_from_user_input(
            result.term, result.context, vocab_provider, audio_provider
        )
        if not card.is_valid():
            show_warning("Invalid card data.")
            return

        preview_dialog_result = show_card_preview_dialog(mw, card)
        if preview_dialog_result.result == CardPreviewResult.SAVE:
            try:
                anki_service = AnkiService(mw, MODEL_NAME, TEMPLATE_NAME)
                removed = anki_service.save_card(card, result.selected_deck_id)
                success_message = f"German card created: {card.term}"
                if removed:
                    success_message += f", Removed duplicate cards: {removed}"
                show_info(success_message)
                return
            except Exception as e:
                show_warning(f"Failed to create card: {str(e)}")
                return
        elif preview_dialog_result.result == CardPreviewResult.CANCEL:
            return
        elif preview_dialog_result.result == CardPreviewResult.REGENERATE:
            # Update context if provided
            if preview_dialog_result.updated_context is not None:
                result.context = preview_dialog_result.updated_context
            continue

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action)
