"""OpenAI-based implementation of the :class:`VocabProvider` interface."""

from __future__ import annotations

import json
import os
from string import Template
from typing import Any, Optional

from .vocab_provider import VocabItem


class _RequestsOpenAIClient:
    """Minimal OpenAI client using requests to avoid binary deps."""

    def __init__(self, api_key: Optional[str], requests_module: Any) -> None:
        self.api_key = api_key
        self._requests = requests_module
        self._session = requests_module.Session()
        self.chat = _ChatNamespace(self)

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise ValueError("OpenAI API key is missing")

        response = self._session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"OpenAI API returned invalid JSON (status {response.status_code})"
            ) from exc

        if response.status_code >= 400:
            message = (
                data.get("error", {}).get("message")
                if isinstance(data, dict)
                else None
            )
            raise RuntimeError(
                message or f"OpenAI API error (status {response.status_code})"
            )

        if not isinstance(data, dict):
            raise RuntimeError("OpenAI API returned unexpected response type")

        return data


class _ChatNamespace:
    def __init__(self, client: _RequestsOpenAIClient) -> None:
        self.completions = _ChatCompletions(client)


class _ChatCompletions:
    def __init__(self, client: _RequestsOpenAIClient) -> None:
        self._client = client

    def create(
        self, *, model: str, messages: list[dict[str, str]], temperature: float
    ) -> dict[str, Any]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        return self._client._post(payload)


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
            # Ensures the addon works without requiring users to install
            # dependencies. The vendor directory contains pre-bundled packages
            # (requests, etc.) that are included with the addon distribution.
            try:
                import sys

                # Get the addon directory (plugin/__init__.py is the entry point)
                addon_dir = os.path.dirname(os.path.dirname(__file__))
                vendor_dir = os.path.join(addon_dir, "vendor")

                if os.path.exists(vendor_dir) and vendor_dir not in sys.path:
                    sys.path.insert(0, vendor_dir)

                import requests
            except ImportError as exc:
                raise ImportError(
                    "The 'requests' package is missing. Please ensure the addon "
                    "was bundled correctly."
                ) from exc

            self._openai = _RequestsOpenAIClient(api_key, requests)
        else:
            self._openai = openai_client
            if hasattr(self._openai, "api_key"):
                # Allow tests to inject a client without requiring network calls.
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

        content = self._extract_content(response)
        if content is None:
            raise ValueError("OpenAI returned empty response")
        data = json.loads(content)
        return VocabItem(
            term=data.get("term", term),
            term_translation=data.get("term_translation", ""),
            sentence=data.get("sentence", ""),
            sentence_translation=data.get("sentence_translation", ""),
        )

    @staticmethod
    def _extract_content(response: Any) -> str:
        if isinstance(response, dict):
            choices = response.get("choices") or []
            if not choices:
                raise ValueError("OpenAI returned no choices")
            first_choice = choices[0]
            message = (
                first_choice.get("message")
                if isinstance(first_choice, dict)
                else None
            )
            content = message.get("content") if isinstance(message, dict) else None
            if content is None:
                raise ValueError("OpenAI returned empty response")
            if not isinstance(content, str):
                raise ValueError("OpenAI returned non-text response")
            return content

        choices = getattr(response, "choices", None)
        if not choices:
            raise ValueError("OpenAI returned no choices")
        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", None) if message is not None else None
        if content is None:
            raise ValueError("OpenAI returned empty response")
        if not isinstance(content, str):
            raise ValueError("OpenAI returned non-text response")
        return content
