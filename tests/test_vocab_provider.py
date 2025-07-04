import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.vocab_provider import VocabProvider


class FakeChatCompletion:
    def __init__(self, content):
        self.content = content
        self.last_args = None

    def create(self, model, messages, temperature):
        self.last_args = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        # Simulate OpenAI response object structure
        class _Message:
            def __init__(self, c):
                self.content = c
        class _Choice:
            def __init__(self, c):
                self.message = _Message(c)
        class _Response:
            def __init__(self, c):
                self.choices = [_Choice(c)]
        return _Response(self.content)


class FakeOpenAI:
    def __init__(self, content):
        self.ChatCompletion = FakeChatCompletion(content)
        self.api_key = None


def test_get_vocab():
    json_resp = '{"term":"der Hund","term_translation":"dog","sentence":"Der Hund bellt.","sentence_translation":"The dog barks."}'
    fake_client = FakeOpenAI(json_resp)
    provider = VocabProvider("test", "English", openai_client=fake_client)
    data = provider.get_vocab("Hund", "")

    assert data["term"] == "der Hund"
    assert fake_client.ChatCompletion.last_args is not None
    system_msg = fake_client.ChatCompletion.last_args["messages"][0]["content"]
    assert "English" in system_msg

