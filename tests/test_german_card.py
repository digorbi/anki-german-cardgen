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

if __name__ == "__main__":
    test_german_card_creation()
    test_german_card_invalid()
    print("All tests passed!") 