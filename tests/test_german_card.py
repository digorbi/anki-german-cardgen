import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.german_card import GermanCard
from core.vocab_provider import VocabProvider, VocabItem


class DummyProvider(VocabProvider):
    def get_vocab(self, term, context: str = "") -> VocabItem:
        return VocabItem(
            term=term,
            term_translation=f"{term}_t",
            sentence=f"S {term}",
            sentence_translation=f"ST {term}",
        )

def test_german_card_creation():
    card = GermanCard(
        term="Haus",
        context="Das Haus ist groß.",
        audio_path="test.mp3"
    )

    assert card.term == "Haus"
    assert card.context == "Das Haus ist groß."
    assert card._audio_filename == "[sound:test.mp3]"
    assert card.is_valid() == True

def test_german_card_invalid():
    card = GermanCard(term="", context="Test", audio_path="")
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

    for term, expected_id in test_cases:
        card = GermanCard(term=term, context="Test", audio_path="")
        assert card._id == expected_id, f"Failed for term: '{term}', expected: '{expected_id}', got: '{card._id}'"

def test_create_from_user_input():
    card = GermanCard.create_from_user_input(
        "Hund", "", "bark.mp3", DummyProvider()
    )
    assert card.term == "Hund"
    assert card.context == ""
    assert card.sentence == "S Hund"
    assert card.term_translation == "Hund_t"
    assert card.sentence_translation == "ST Hund"

if __name__ == "__main__":
    test_german_card_creation()
    test_german_card_invalid()
    test_gen_id()
    print("All tests passed!")
