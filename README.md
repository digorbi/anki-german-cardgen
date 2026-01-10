# German Card Generator for Anki – AI-powered examples &amp; audio

A Python-based Anki plugin that generates German vocabulary cards with AI-powered example sentences and audio pronunciation. The plugin integrates seamlessly with Anki Desktop to create rich, contextual learning cards for German language learners.

## 🎯 Project Overview

This project aims to streamline the creation of high-quality German vocabulary cards by:
- Automatically generating contextual example sentences using AI
- Creating audio pronunciations for proper German pronunciation
- Providing a user-friendly interface within Anki
- Supporting different word types (nouns, verbs, adjectives, phrases)

## 🖥️ Installation

- **Supported only on macOS** (Intel `x86_64` and Apple Silicon `arm64`)
- Download the [latest release](https://github.com/digorbi/anki-german-cardgen/releases)
- Unzip it into your Anki add-ons folder: `~/Library/Application Support/Anki2/addons21/`
- After unzipping, the structure should look like: `~/Library/Application Support/Anki2/addons21/anki-german-cardgen/`

### No native dependency requirement

The addon now uses a pure-Python HTTP client for OpenAI, so you should not see
macOS quarantine errors from binary wheels. If you are upgrading from an older
release that bundled native OpenAI dependencies, remove the old addon folder
and reinstall the latest release.

---
> 🚧 **This project is under active development.**
>
> Some features may be incomplete or not fully stable yet. If you'd like to help improve the plugin or report issues, check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
