from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

from aqt.qt import (  # type: ignore
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
from aqt.utils import showInfo, showWarning  # type: ignore

from core.german_card import GermanCard


class CardPreviewResult(Enum):
    SAVE = auto()
    CANCEL = auto()
    REGENERATE = auto()

@dataclass
class CardInputResult:
    term: str
    selected_deck_id: int
    context: str

@dataclass
class SettingsResult:
    api_key: str
    target_language: str
    desired_template: str

@dataclass
class CardPreviewDialogResult:
    result: CardPreviewResult
    updated_context: Optional[str] = None


def get_settings_dialog(
    mw: Any,
    api_key: str,
    target_language: str
) -> Optional[SettingsResult]:
    """Prompt for OpenAI API settings and return SettingsResult or None."""
    dialog = QDialog(mw)
    dialog.setWindowTitle("OpenAI Settings")
    layout = QVBoxLayout(dialog)

    key_label = QLabel("OpenAI API key:")
    key_input = QLineEdit(api_key)
    key_input.setEchoMode(QLineEdit.EchoMode.Password)
    layout.addWidget(key_label)
    layout.addWidget(key_input)

    lang_label = QLabel("Default translation language:")
    lang_input = QLineEdit(target_language)
    layout.addWidget(lang_label)
    layout.addWidget(lang_input)

    # Template selection
    template_label = QLabel("Select template:")
    template_combo = QComboBox()
    template_combo.addItem("Word Template", GermanCard.CARD_TEMPLATE_WORD)
    template_combo.addItem("Sentence Template", GermanCard.CARD_TEMPLATE_SENTENCE)
    layout.addWidget(template_label)
    layout.addWidget(template_combo)

    buttons = QHBoxLayout()
    ok_button = QPushButton("Save")
    cancel_button = QPushButton("Cancel")
    buttons.addWidget(ok_button)
    buttons.addWidget(cancel_button)
    layout.addLayout(buttons)

    ok_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return None

    return SettingsResult(
        api_key=key_input.text().strip(),
        target_language=lang_input.text().strip(),
        desired_template=template_combo.currentData()
    )

def get_card_input_dialog(mw: Any) -> Optional[CardInputResult]:
    """
    Show the card input dialog and return CardInputResult or None if cancelled.
    """
    dialog = QDialog(None)
    dialog.setWindowTitle("German Card Generator")
    dialog.setModal(True)

    layout = QVBoxLayout()

    # Term input
    term_label = QLabel("Enter German term:")
    term_input = QLineEdit()
    layout.addWidget(term_label)
    layout.addWidget(term_input)

    # Context input (multiline)
    context_label = QLabel("Context (optional):")
    context_input = QTextEdit()
    context_input.setMinimumHeight(80)  # Make it big
    layout.addWidget(context_label)
    layout.addWidget(context_input)

    # Deck selection
    deck_label = QLabel("Select deck:")
    deck_combo = QComboBox()
    decks = mw.col.decks.all()
    current_deck_id = mw.col.decks.current()['id']
    current_deck_name = ""
    for deck in decks:
        deck_name = deck['name']
        deck_combo.addItem(deck_name, deck['id'])
        if deck['id'] == current_deck_id:
            current_deck_name = deck_name
    if current_deck_name:
        index = deck_combo.findText(current_deck_name)
        if index >= 0:
            deck_combo.setCurrentIndex(index)
    layout.addWidget(deck_label)
    layout.addWidget(deck_combo)

    # Buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("Generate Card")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    dialog.setLayout(layout)
    ok_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return None

    term = term_input.text().strip()
    context = context_input.toPlainText().strip()
    selected_deck_id = deck_combo.currentData()
    return CardInputResult(term, selected_deck_id, context)

def show_info(message: str) -> None:
    showInfo(message)

def show_warning(message: str) -> None:
    showWarning(message)

def show_card_preview_dialog(mw: Any, card: GermanCard) -> CardPreviewDialogResult:
    """
    Show a preview dialog of the card before saving.
    Returns:
        CardPreviewDialogResult with:
        - result: One of:
            CardPreviewResult.SAVE: User accepted the card
            CardPreviewResult.CANCEL: User canceled card creation
            CardPreviewResult.REGENERATE: User requested to regenerate the card
        - updated_context: The updated context when result is REGENERATE, None otherwise
    """
    dialog = QDialog(mw)
    dialog.setWindowTitle("Card Preview")
    dialog.setMinimumWidth(400)

    layout = QVBoxLayout()

    # Front preview
    front_group = QVBoxLayout()
    front_label = QLabel("<b>Front:</b>")
    front_content = QLabel(
        f"<div><b>{card.term}</b></div>"
        f"<div>{card.sentence}</div>"
    )
    front_content.setWordWrap(True)
    front_group.addWidget(front_label)
    front_group.addWidget(front_content)
    layout.addLayout(front_group)

    # Back preview
    back_group = QVBoxLayout()
    back_label = QLabel("<b>Back:</b>")
    back_content = QLabel(
        f"<div><b>{card.term}</b></div>"
        f"<div>{card.term_translation}</div>"
        f"<div>{card.sentence}</div>"
        f"<div>{card.sentence_translation}</div>"
        f"<div><i>{card.context}</i></div>"
    )
    back_content.setWordWrap(True)
    back_group.addWidget(back_label)
    back_group.addWidget(back_content)
    layout.addLayout(back_group)

    # Context input for regeneration
    context_group = QVBoxLayout()
    context_label = QLabel("<b>Context (edit to regenerate with new context):</b>")
    context_input = QTextEdit()
    context_input.setPlainText(card.context)
    context_input.setMinimumHeight(80)
    context_group.addWidget(context_label)
    context_group.addWidget(context_input)
    layout.addLayout(context_group)

    # Buttons
    button_layout = QHBoxLayout()
    save_button = QPushButton("Save Card")
    regenerate_button = QPushButton("Regenerate")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(save_button)
    button_layout.addWidget(regenerate_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    dialog.setLayout(layout)

    # Store the result
    result = CardPreviewResult.CANCEL  # Default result if dialog is closed
    updated_context = None

    def on_save() -> None:
        nonlocal result
        result = CardPreviewResult.SAVE
        dialog.accept()

    def on_regenerate() -> None:
        nonlocal result, updated_context
        result = CardPreviewResult.REGENERATE
        updated_context = context_input.toPlainText().strip()
        dialog.accept()

    def on_cancel() -> None:
        nonlocal result
        result = CardPreviewResult.CANCEL
        dialog.accept()

    save_button.clicked.connect(on_save)
    regenerate_button.clicked.connect(on_regenerate)
    cancel_button.clicked.connect(on_cancel)

    dialog.exec()
    return CardPreviewDialogResult(result=result, updated_context=updated_context)
