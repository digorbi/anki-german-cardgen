from .model import GermanCard

def ensure_german_model_exists(mw):
    model_name = "GermanCardModel"
    existing = mw.col.models.by_name(model_name)
    if existing:
        return existing
    model = mw.col.models.new(model_name)
    for field in ["id", "de_word", "de_sentence", "de_audio", "word_translation", "sentence_translation", "note"]:
        mw.col.models.add_field(model, mw.col.models.new_field(field))
    template = mw.col.models.new_template("German → English")
    template['qfmt'] = """
<div class=\"german-word\">{{de_word}}</div>
<div class=\"german-sentence\">{{de_sentence}}</div>
{{de_audio}}
"""
    template['afmt'] = """
<div class=\"german-word\">{{de_word}}</div>
<div class=\"word-translation\">{{word_translation}}</div>
<div class=\"german-sentence\">{{de_sentence}}</div>
<div class=\"sentence-translation\">{{sentence_translation}}</div>
{{de_audio}}
<div class=\"notes\">{{note}}</div>
"""
    mw.col.models.add_template(model, template)
    mw.col.models.add(model)
    return model

def german_card_to_anki_note(card: GermanCard, mw, model):
    note = mw.col.new_note(model)
    fields = card.to_fields_list()
    for i, value in enumerate(fields):
        note.fields[i] = value
    return note 