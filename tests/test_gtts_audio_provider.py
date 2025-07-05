import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.gtts_audio_provider import GttsAudioProvider


class _FakeGttsInstance:
    def __init__(self):
        self.written = False

    def write_to_fp(self, fp):
        fp.write(b"dummy")
        self.written = True


class _FakeGttsFactory:
    def __init__(self):
        self.last_kwargs = None

    def __call__(self, text, lang="de"):
        self.last_kwargs = {"text": text, "lang": lang}
        return _FakeGttsInstance()


def test_get_audio_and_filename():
    factory = _FakeGttsFactory()
    provider = GttsAudioProvider(lang="de", gtts_factory=factory)

    data = provider.get_audio("Hallo")

    assert data == b"dummy"
    assert factory.last_kwargs == {"text": "Hallo", "lang": "de"}
    assert provider.get_file_name("card1") == "card1_gtts.mp3"
