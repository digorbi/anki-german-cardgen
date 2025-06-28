import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.german_card import GermanCard

def test_german_card_creation():
    card = GermanCard(
        word="Haus",
        example_sentence="Das Haus ist groß.",
        word_translation="house",
        sentence_translation="The house is big."
    )
    
    assert card.word == "Haus"
    assert card.example_sentence == "Das Haus ist groß."
    assert card.word_translation == "house"
    assert card.is_valid() == True

def test_german_card_invalid():
    card = GermanCard(word="", example_sentence="Test")
    assert card.is_valid() == False

def test_gen_id():
    """Test ID generation with table-driven tests"""
    test_cases = [
        # Basic words
        ("Haus", "haus"),
        ("Auto", "auto"),
        
        # Words with spaces
        ("Das Haus", "das_haus"),
        ("Ein schönes Auto", "ein_schoenes_auto"),
        
        # German umlauts
        ("Mädchen", "maedchen"),
        ("König", "koenig"),
        ("Bücher", "buecher"),
        ("Straße", "strasse"),
        
        # Special characters
        ("Haus!", "haus"),
        ("Auto@#$%", "auto"),
        ("Test-Wort", "testwort"),
        ("Wort123", "wort123"),
        
        # Mixed case
        ("HAUS", "haus"),
        ("HaUs", "haus"),
        
        # Numbers
        ("Auto2023", "auto2023"),
        ("123Haus", "123haus"),
        
        # Complex examples
        ("Schlüssel", "schluessel"),
        ("Müller", "mueller"),
        ("Königsberg", "koenigsberg"),
        ("Größe", "groesse"),
        
        # Edge cases
        ("", ""),
        ("!@#$%^&*()", ""),
        ("   ", "___"),
        ("test_word", "test_word"),
    ]
    
    for word, expected_id in test_cases:
        card = GermanCard(word=word, example_sentence="Test")
        assert card._id == expected_id, f"Failed for word: '{word}', expected: '{expected_id}', got: '{card._id}'"

if __name__ == "__main__":
    test_german_card_creation()
    test_german_card_invalid()
    test_gen_id()
    print("All tests passed!") 