from aqt.qt import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

class CardInputResult:
    def __init__(self, word, selected_deck_id, audio_path):
        self.word = word
        self.selected_deck_id = selected_deck_id
        self.audio_path = audio_path

def get_card_input_dialog(mw):
    """
    Show the card input dialog and return CardInputResult or None if cancelled.
    """
    dialog = QDialog(None)
    dialog.setWindowTitle("German Card Generator")
    dialog.setModal(True)

    layout = QVBoxLayout()

    # Word input
    word_label = QLabel("Enter German word:")
    word_input = QLineEdit()
    layout.addWidget(word_label)
    layout.addWidget(word_input)

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

    # Audio file path input
    audio_label = QLabel("Audio file path (optional):")
    audio_input = QLineEdit()
    audio_input.setPlaceholderText("e.g., /path/to/audio.mp3")
    layout.addWidget(audio_label)
    layout.addWidget(audio_input)

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

    word = word_input.text().strip()
    selected_deck_id = deck_combo.currentData()
    audio_path = audio_input.text().strip()
    return CardInputResult(word, selected_deck_id, audio_path)

def show_info(message):
    from aqt.utils import showInfo
    showInfo(message)

def show_warning(message):
    from aqt.utils import showWarning
    showWarning(message) 