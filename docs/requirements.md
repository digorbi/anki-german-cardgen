# Software Requirements

## POC scope
- [X] FR1: Generate simple Anki card using plugin — input text and audio, select deck.
- [X] NFR1: Run project locally without Anki (test logic in CLI or script)

## MVP Scope
### Functional Requirements
- [ ] FR2: User can input a word + optional context
- [ ] FR3: Plugin detects word type (noun, verb, adjective, phrase)
- [ ] FR4: Plugin generates tailored example sentence(s) using OpenAI
- [ ] FR5: Card template adapts based on word type
- [ ] FR6: User can regenerate content before saving
- [ ] FR7: Audio is generated via gTTS and attached to the card
- [ ] FR8: User can configure API key and language settings
- [ ] FR9: Select or create target deck for card insertion

### Non-Functional Requirements
- [ ] NFR2: Minimal, intuitive UI for configuration and generation (Qt-based)
- [ ] NFR3: Compatible with Anki Desktop 2.1+
- [ ] NFR4: No crash if config is missing or API fails — show UI warnings
- [ ] NFR5: Clear logs or messages for debugging in dev mode
- [ ] NFR6: Plugin logic is modular and testable outside Anki