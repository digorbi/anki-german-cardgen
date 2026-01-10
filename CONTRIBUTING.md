# 🤝 Contributing

## 🏗️ Architecture & Project Structure

### 🎯 **`core/`** - Core Business Logic
Contains the heart of the application - the card models and business logic that are independent of Anki. This layer can be tested and used without Anki integration.

### 🔌 **`plugin/`** - Anki Integration Layer
Handles all Anki-specific functionality including the user interface, plugin lifecycle, and integration with Anki's API. This is what gets installed into Anki.

### 📝 **`prompts/`** - Prompt Templates
Reusable system, user, and assistant prompts for language model interactions.

### ⚙️ **`scripts/`** - Utility Scripts
Automation helpers for bundling and deploying the plugin.

### 🖌️ **`templates/`** - Card Templates
HTML and CSS layouts used for the generated cards.

### 🧪 **`tests/`** - Test Suite
Pytest-based checks covering both the core and plugin layers.

## 🏗️ Setup

### Prerequisites
- Python 3.9+
- Anki Desktop 2.1+
- Virtual environment (recommended)

### Python setup
```bash
# 1. Create a virtual environment (Python version is set by .python-version if using pyenv)
python -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate   # On macOS/Linux
# .venv\\Scripts\\activate  # On Windows

# 3. Install production dependencies
pip install -r requirements.txt

# 4. (For development) Install dev dependencies
pip install -r requirements-dev.txt
....
```

### Unit Tests
The project uses pytest for testing. To run the test suite:

```bash
# Run all tests
pytest
```

### Integration Tests
Integration tests are marked with `@pytest.mark.integration` and are skipped
unless the required environment variables are set.

- OpenAI integration: requires `OPENAI_API_KEY`
- gTTS integration: requires `GTTS_ENABLED=true`

Examples:

```bash
# Run only integration tests with OpenAI enabled
OPENAI_API_KEY=sk-... pytest -m integration

# Run only integration tests with gTTS enabled
GTTS_ENABLED=true pytest -m integration

# Run all integration tests
OPENAI_API_KEY=sk-... GTTS_ENABLED=true pytest -m integration
```

These tests call external services and may incur cost or require network access.

### Linting & Static Analysis
Code style and static analysis are enforced with [ruff](https://docs.astral.sh/ruff/) and [mypy](http://mypy-lang.org/). These checks run automatically in CI, but you can run them locally:

```bash
# Run linter
ruff check .

# Run static type checks
mypy .
```

## Manual Testing
Bundle dependencies into vendor folder for deployment

```bash
# be aware of the correct python version
python scripts/bundle.py
```

Copy the `plugin/` directory to your Anki plugins folder. The `core` folder has to be copied inside. 
Use the following automation:

```bash
# Deploy plugin to Anki
python scripts/deploy.py
```

- Restart Anki
- The plugin should appear in Tools → German Card Generator

## 🔧 Troubleshooting

### OpenAI API Quota Issues
If integration tests fail with Error code: 429 - "quota exceeded" error: you need to top up your balance at [OpenAI Platform](https://platform.openai.com/). Tests cost pennies.

### Plugin Not Appearing in Anki
- Restart Anki after deployment
- Check Tools → German Card Generator menu

### Plugin crashes in Anki with a "package is missing" error
- Install dependencies into the `plugin/vendor` folder using: `./scripts/bundle.py`

### Binary dependency errors (e.g. `No module named 'pydantic_core._pydantic_core'`). 
- Make sure to bundle dependencies using the same Python version as your Anki build. The `.so` files in `vendor` must match Anki's Python version.
