"""OpenAI-based implementation of the :class:`VocabProvider` interface."""

from __future__ import annotations

import json
import os
from string import Template
from typing import Any, Optional

from .vocab_provider import VocabItem


class OpenaiVocabProvider:
    """Retrieve vocabulary data using OpenAI chat completion."""

    def __init__(
        self,
        api_key: str,
        target_language: str,
        *,
        model: str = "gpt-3.5-turbo",
        openai_client: Optional[Any] = None,
    ) -> None:
        if openai_client is None:
            # Try to import from bundled vendor directory first
            # This ensures the addon works without requiring users to install dependencies
            # The vendor directory contains pre-bundled packages (openai, requests, etc.)
            # that are included with the addon distribution
            try:
                import sys

                # Get the addon directory (plugin/__init__.py is the entry point)
                addon_dir = os.path.dirname(os.path.dirname(__file__))
                vendor_dir = os.path.join(addon_dir, "vendor")

                if os.path.exists(vendor_dir) and vendor_dir not in sys.path:
                    sys.path.insert(0, vendor_dir)

                import openai
                self._openai = openai
            except ImportError:
                raise ImportError(
                    "The 'openai' package is missing. Please ensure the addon was bundled correctly."
                )
        else:
            self._openai = openai_client

        # ``api_key`` might be ``None`` – the real OpenAI library will raise an
        # exception when used without a key.  We simply assign it to allow tests
        # to run without contacting the network.
        self._openai.api_key = api_key

        self.target_language = target_language
        self.model = model

        prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        self._system_template = self._load_template(prompts_dir, "vocab.system.md")
        self._assistant_template = self._load_template(
            prompts_dir, "vocab.assistant.md"
        )
        self._user_template = self._load_template(prompts_dir, "vocab.user.md")

    @staticmethod
    def _load_template(directory: str, filename: str) -> Template:
        path = os.path.join(directory, filename)
        with open(path, encoding="utf-8") as fh:
            return Template(fh.read())

    def get_vocab(self, term: str, context: str = "") -> VocabItem:
        system_msg = self._system_template.substitute(
            target_language=self.target_language
        )
        assistant_msg = self._assistant_template.template
        user_msg = self._user_template.substitute(
            term=term, target_language=self.target_language, context=context
        )

        response = self._openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "assistant", "content": assistant_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI returned empty response")
        data = json.loads(content)
        return VocabItem(
            term=data.get("term", term),
            term_translation=data.get("term_translation", ""),
            sentence=data.get("sentence", ""),
            sentence_translation=data.get("sentence_translation", ""),
        )
