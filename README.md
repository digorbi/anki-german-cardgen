# German Card Generator for Anki – AI-powered examples &amp; audio

A Python-based Anki plugin that generates German vocabulary cards with AI-powered example sentences and audio pronunciation. The plugin integrates seamlessly with Anki Desktop to create rich, contextual learning cards for German language learners.

## 🎯 Project Overview

This project aims to streamline the creation of high-quality German vocabulary cards by:
- Automatically generating contextual example sentences using AI
- Creating audio pronunciations for proper German pronunciation
- Providing a user-friendly interface within Anki
- Supporting different word types (nouns, verbs, adjectives, phrases)

## 🏗️ Architecture & Project Structure

```
anki-german-cardgen/
├── 📂 core/                   # Core business logic and card models
│   ├── german_card.py         # GermanCard class - main card model
│   └── audio_card.py          # Abstract AudioCard base class
│
├── 📂 plugin/                  # Anki plugin integration layer
│   ├── anki_service.py        # Anki API integration and card management
│   ├── view.py                # Qt-based user interface components
│   └── manifest.json          # Anki plugin metadata and configuration
│
├── 📂 tests/                   # Test suite and test utilities
│
├── 📂 docs/                    # Project documentation
│
├── 📂 scripts/                 # Build, deployment, and utility scripts
│   └── deploy.sh              # Mac deployment script for Anki plugin
```

### Packages Descriptions

#### 🎯 **`core/`** - Core Business Logic
Contains the heart of the application - the card models and business logic that are independent of Anki. This layer can be tested and used without Anki integration.

#### 🔌 **`plugin/`** - Anki Integration Layer
Handles all Anki-specific functionality including the user interface, plugin lifecycle, and integration with Anki's API. This is what gets installed into Anki.

## 🚀 Contributing

### Prerequisites
- Python 3.7+
- Anki Desktop 2.1+
- Virtual environment (recommended)

### Manual Testing
Copy the `plugin/` directory to your Anki plugins folder. The `core` folder has to be copied inside. 
Use the following automation:

```bash
# Deploy plugin to Anki
./scripts/deploy.sh 
```

- Restart Anki
- The plugin should appear in Tools → German Card Generator

### Unit Tests
The project uses pytest for testing. To run the test suite:

```bash
# Run all tests
pytest
```

---

**Note**: This project is currently in active development. The plugin may not be fully functional for all features listed in the requirements.
