from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

def generate_card():
    word = QInputDialog.getText(None, "German Card", "Enter German word:")[0]
    if word:
        model = mw.col.models.by_name("Basic")
        mw.col.models.set_current(model)
        note = mw.col.new_note(model)
        note.fields[0] = word
        note.fields[1] = f"German word: {word}"
        mw.col.add_note(note, mw.col.decks.current()['id'])
        mw.col.save()
        showInfo("Card created!")

action = QAction("German Card", mw)
action.triggered.connect(generate_card)
mw.form.menuTools.addAction(action) 