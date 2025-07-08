import os
import sys

import pytest

# Add the parent directory to the path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.german_card import GermanCard
from core.gtts_audio_provider import GttsAudioProvider
from core.openai_vocab_provider import OpenaiVocabProvider
from core.vocab_provider import VocabItem

# Import the real OpenAI client for testing
try:
    import openai
except ImportError:
    pytest.skip("OpenAI package not installed - skipping integration test")

# Import gTTS for audio integration testing
try:
    from gtts import gTTS  # noqa: F401
except ImportError:
    pytest.skip("gTTS package not installed - skipping integration test")


class DummyProvider:
    def get_vocab(self, term: str, context: str = "") -> VocabItem:
        return VocabItem(
            term=term,
            term_translation=f"{term}_t",
            sentence=f"S {term}",
            sentence_translation=f"ST {term}",
        )


class DummyAudioProvider:
    def get_audio(self, text: str) -> bytes:
        return b"dummy"

    def get_file_name(self, base: str) -> str:
        return f"{base}_dummy.mp3"

@pytest.mark.integration
def test_german_card_openai_integration():
    """Integration test for GermanCard creation with real OpenAI vocab provider."""

    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip(
            "OPENAI_API_KEY environment variable not set - skipping integration test"
        )

    # Test parameters
    test_term = "Haus"
    test_context = "A1 level German"

    try:
        # Create real OpenAI vocab provider with explicit OpenAI client
        vocab_provider = OpenaiVocabProvider(
            api_key=api_key,
            target_language="English",
            openai_client=openai
        )

        # Create GermanCard using the real provider
        card = GermanCard.create_from_user_input(
            term=test_term,
            context=test_context,
            vocab_provider=vocab_provider,
            audio_provider=DummyAudioProvider()
        )

        # Verify the card was created successfully
        assert card is not None
        assert card.is_valid()

        # Verify that the vocab provider populated the card with data
        assert card.sentence != "", "Sentence should be populated by OpenAI"
        assert card.term_translation != "", (
            "Term translation should be populated by OpenAI"
        )
        assert card.sentence_translation != "", (
            "Sentence translation should be populated by OpenAI"
        )

        print(f"✅ Integration test passed! Created card for term: '{test_term}'")
        print(f"   Updated Term: {card.term}")
        print(f"   Term Translation: {card.term_translation}")
        print(f"   Sentence: {card.sentence}")
        print(f"   Sentence Translation: {card.sentence_translation}")

    except Exception as e:
        pytest.fail(f"Integration test failed with error: {str(e)}")

@pytest.mark.integration
def test_gtts_audio_provider_integration():
    """Integration test for audio generation using gTTS."""

    if os.getenv("GTTS_ENABLED") != "true":
        pytest.skip(
            "GTTS_ENABLED environment variable not set to 'true' - "
            "skipping integration test"
        )

    from gtts import gTTS

    card = GermanCard.create_from_user_input(
        term="Haus",
        context="",
        vocab_provider=DummyProvider(),
        audio_provider=GttsAudioProvider("de", gtts_factory=gTTS),
    )

    assert card.get_audio_data() is not None
    assert isinstance(card.get_audio_data(), bytes)
    assert card.get_audio_filename().endswith("_gtts.mp3")


if __name__ == "__main__":
    test_german_card_openai_integration()
    test_gtts_audio_provider_integration()
