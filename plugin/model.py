from aqt import mw

def create_german_model():
    """Create a custom German learning model if it doesn't exist"""
    model_name = "German Card"
    
    # Check if model already exists
    model = mw.col.models.by_name(model_name)
    if model:
        return model
    
    # Create new model
    model = mw.col.models.new(model_name)
    
    # Add fields based on the specified structure
    fields = [
        "id",
        "de_word",
        "de_sentence", 
        "de_audio",
        "word_translation",
        "sentence_translation",
        "note"
    ]
    
    for field_name in fields:
        mw.col.models.add_field(model, mw.col.models.new_field(field_name))
    
    # Create card template
    template = mw.col.models.new_template("German → English")
    
    # Question format (front of card)
    template['qfmt'] = """
<div class="german-word">{{de_word}}</div>
<div class="german-sentence">{{de_sentence}}</div>
{{de_audio}}
"""
    
    # Answer format (back of card)
    template['afmt'] = """
<div class="german-word">{{de_word}}</div>
<div class="word-translation">{{word_translation}}</div>
<div class="german-sentence">{{de_sentence}}</div>
<div class="sentence-translation">{{sentence_translation}}</div>
{{de_audio}}
<div class="notes">{{note}}</div>
"""
    
    mw.col.models.add_template(model, template)
    mw.col.models.add(model)
    mw.col.save()
    
    return model 