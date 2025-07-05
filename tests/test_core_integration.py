import os
import sys
import pytest

# Add the parent directory to the path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.german_card import GermanCard
from core.openai_vocab_provider import OpenaiVocabProvider

# Import the real OpenAI client for testing
try:
    import openai
except ImportError:
    pytest.skip("OpenAI package not installed - skipping integration test")


def test_german_card_openai_integration():
    """Integration test for GermanCard creation with real OpenAI vocab provider."""
    
    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable not set - skipping integration test")
    
    # Test parameters
    test_term = "Haus"
    test_context = "A1 level German"
    test_audio_path = "test_audio.mp3"
    
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
            audio_path=test_audio_path,
            vocab_provider=vocab_provider
        )
        
        # Verify the card was created successfully
        assert card is not None
        assert card.is_valid() == True
        
        # Verify that the vocab provider populated the card with data
        assert card.sentence != "", "Sentence should be populated by OpenAI"
        assert card.term_translation != "", "Term translation should be populated by OpenAI"
        assert card.sentence_translation != "", "Sentence translation should be populated by OpenAI"
        
        print(f"✅ Integration test passed! Created card for term: '{test_term}'")
        print(f"   Updated Term: {card.term}")
        print(f"   Term Translation: {card.term_translation}")
        print(f"   Sentence: {card.sentence}")
        print(f"   Sentence Translation: {card.sentence_translation}")
        
    except Exception as e:
        pytest.fail(f"Integration test failed with error: {str(e)}")


if __name__ == "__main__":
    test_german_card_openai_integration()
