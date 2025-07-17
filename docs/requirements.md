# Software Requirements

## POC scope
- [X] FR1: Generate simple Anki card using plugin — input text and audio, select deck.
- [X] NFR1: Run project locally without Anki (test logic in CLI or script)

## MVP Scope
### Functional Requirements
- [X] FR2: User can input a word + optional context
- [X] FR3: Plugin detects word type (noun, verb, adjective, phrase)
- [X] FR4: Plugin generates tailored example sentence(s) using OpenAI
- [ ] FR5: Card template adapts based on word type
- [X] FR6: User can regenerate content before saving
- [X] FR7: Audio is generated via gTTS and attached to the card
- [X] FR8: User can configure API key and language settings
- [X] FR9: Select or create target deck for card insertion

### Non-Functional Requirements
- [X] NFR2: Minimal, intuitive UI for configuration and generation (Qt-based)
- [X] NFR3: Compatible with Anki Desktop 2.1+
- [X] NFR4: No crash if config is missing or API fails — show UI warnings
- [X] NFR5: Clear logs or messages for debugging in dev mode
- [X] NFR6: Plugin logic is modular and testable outside Anki
- [X] NFR7: Build plugin releases using github CI/CD
- [X] NFR8: Refactor AudioCard and simplify interface by reducing methods, use maps and remove Optinal