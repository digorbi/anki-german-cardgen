"""Utilities for retrieving vocabulary data from OpenAI.

This module defines :class:`VocabProvider` which wraps a ChatGPT style API call
and returns structured JSON describing the requested vocabulary term.  The class
loads prompt templates from the ``prompts`` directory located at the project
root.  For ease of testing an ``openai_client`` can be injected, so unit tests do
not depend on the real OpenAI package or network access.
"""

from __future__ import annotations

import json
import os
from string import Template
from typing import Any, Dict, Optional


class VocabProvider:
    """Retrieve vocabulary data using OpenAI chat completion."""

    def __init__(
        self,
        api_key: str,
        target_language: str,
        *,
        model: str = "gpt-3.5-turbo",
        openai_client: Optional[Any] = None,
    ) -> None:
        """Create a provider instance.

        Parameters
        ----------
        api_key:
            OpenAI API key.
        target_language:
            Language into which translations should be produced.
        model:
            Chat completion model name. Defaults to ``gpt-3.5-turbo``.
        openai_client:
            Optional object compatible with the ``openai`` package.  Used to
            facilitate testing by injecting a fake client.
        """

        if openai_client is None:
            import openai  # type: ignore

            self._openai = openai
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

    def get_vocab(self, term: str, context: str = "") -> Dict[str, str]:
        """Return vocabulary information for ``term``.

        The returned dictionary contains ``term``, ``term_translation``,
        ``sentence`` and ``sentence_translation`` keys as produced by the chat
        completion model.
        """

        system_msg = self._system_template.substitute(
            target_language=self.target_language
        )
        assistant_msg = self._assistant_template.template
        user_msg = self._user_template.substitute(
            term=term, target_language=self.target_language, context=context
        )

        response = self._openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "assistant", "content": assistant_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )

        # ``openai`` library returns a complex object; we only need the text
        # content of the first choice.
        content = response.choices[0].message.content  # type: ignore[index]
        return json.loads(content)
