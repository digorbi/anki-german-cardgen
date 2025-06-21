from aqt import mw
from aqt.utils import showInfo, showWarning
from aqt.qt import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QAction
from .model import create_german_model
import os
import shutil
from pathlib import Path

def copy_audio_to_media(audio_path):
    """
    Copy audio file to Anki's media folder and return the filename
    """
    if not audio_path or not os.path.exists(audio_path):
        return None
    
    try:
        # Get the original filename
        original_filename = os.path.basename(audio_path)
        
        # Create a unique filename in Anki's media folder
        media_dir = mw.col.media.dir()
        filename = original_filename
        
        # If file already exists, add a number suffix
        counter = 1
        while os.path.exists(os.path.join(media_dir, filename)):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            counter += 1
        
        # Copy the file to Anki's media folder
        destination = os.path.join(media_dir, filename)
        shutil.copy2(audio_path, destination)
        
        return filename
        
    except Exception as e:
        showWarning(f"Error copying audio file: {str(e)}")
        return None

def generate_card():
    # Create a custom dialog for input
    dialog = QDialog(None)
    dialog.setWindowTitle("German Card Generator")
    dialog.setModal(True)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Word input
    word_label = QLabel("Enter German word:")
    word_input = QLineEdit()
    layout.addWidget(word_label)
    layout.addWidget(word_input)
    
    # Deck selection
    deck_label = QLabel("Select deck:")
    deck_combo = QComboBox()
    
    # Get all decks and populate the combo box
    decks = mw.col.decks.all()
    current_deck_id = mw.col.decks.current()['id']
    current_deck_name = ""
    
    for deck in decks:
        deck_name = deck['name']
        deck_combo.addItem(deck_name, deck['id'])
        if deck['id'] == current_deck_id:
            current_deck_name = deck_name
    
    # Set the current deck as default
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
    
    # Connect buttons
    ok_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)
    
    # Show dialog
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return
    
    word = word_input.text().strip()
    selected_deck_id = deck_combo.currentData()
    audio_path = audio_input.text().strip()
    
    if not word:
        showWarning("Please enter a German word.")
        return
    
    # Use the custom German model
    model = create_german_model()
    mw.col.models.set_current(model)
    note = mw.col.new_note(model)
    
    # Handle audio file
    audio_filename = ""
    if audio_path:
        audio_filename = copy_audio_to_media(audio_path)
        if audio_filename:
            # Format for Anki audio: [sound:filename]
            audio_filename = f"[sound:{audio_filename}]"
    
    # Fill in the fields
    note.fields[0] = "1"  # id
    note.fields[1] = word  # de_word
    note.fields[2] = f"Example sentence with {word}"  # de_sentence
    note.fields[3] = audio_filename  # de_audio
    note.fields[4] = f"Translation of {word}"  # word_translation
    note.fields[5] = f"Translation of example sentence"  # sentence_translation
    note.fields[6] = ""  # note
    
    # Add note to the selected deck
    mw.col.add_note(note, selected_deck_id)
    mw.col.save()
    
    if audio_filename:
        showInfo(f"German card created with audio: {word}")
    else:
        showInfo(f"German card created: {word}")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 