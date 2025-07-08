from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTextEdit,
)

class CardInputResult:
    def __init__(self, term, selected_deck_id, context):
        self.term = term
        self.selected_deck_id = selected_deck_id
        self.context = context


def get_api_settings_dialog(mw, api_key: str, target_language: str):
    """Prompt for OpenAI API settings and return (api_key, target_language) or None."""
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

    return key_input.text().strip(), lang_input.text().strip()

def get_card_input_dialog(mw):
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

def show_info(message):
    from aqt.utils import showInfo
    showInfo(message)

def show_warning(message):
    from aqt.utils import showWarning
    showWarning(message)
