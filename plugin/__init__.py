from aqt import mw
from aqt.utils import showInfo, showWarning
from aqt.qt import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QAction
from .model import create_german_model
import os
import shutil
from pathlib import Path
from .view import get_card_input_dialog, CardInputResult

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
    # Get user input from the dialog
    result = get_card_input_dialog(mw)
    if not result:
        return
    word = result.word
    selected_deck_id = result.selected_deck_id
    audio_path = result.audio_path

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
            audio_filename = f"[sound:{audio_filename}]"
    # Fill in the fields
    note.fields[0] = "1"  # id
    note.fields[1] = word  # de_word
    note.fields[2] = f"Example sentence with {word}"  # de_sentence
    note.fields[3] = audio_filename  # de_audio
    note.fields[4] = f"Translation of {word}"  # word_translation
    note.fields[5] = f"Translation of example sentence"  # sentence_translation
    note.fields[6] = ""  # note
    mw.col.add_note(note, selected_deck_id)
    mw.col.save()
    if audio_filename:
        showInfo(f"German card created with audio: {word}")
    else:
        showInfo(f"German card created: {word}")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 