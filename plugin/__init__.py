from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from .model import create_german_model

def generate_card():
    word = QInputDialog.getText(None, "German Card", "Enter German word:")[0]
    if word:
        # Use the custom German model
        model = create_german_model()
        mw.col.models.set_current(model)
        note = mw.col.new_note(model)
        
        # Fill in the fields
        note.fields[0] = "1"  # id
        note.fields[1] = word  # de_word
        note.fields[2] = f"Example sentence with {word}"  # de_sentence
        note.fields[3] = ""  # de_audio
        note.fields[4] = f"Translation of {word}"  # word_translation
        note.fields[5] = f"Translation of example sentence"  # sentence_translation
        note.fields[6] = ""  # note
        
        mw.col.add_note(note, mw.col.decks.current()['id'])
        mw.col.save()
        showInfo("German card created!")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 