# 🤝 Contributing

## 🏗️ Architecture & Project Structure

### 🎯 **`core/`** - Core Business Logic
Contains the heart of the application - the card models and business logic that are independent of Anki. This layer can be tested and used without Anki integration.

### 🔌 **`plugin/`** - Anki Integration Layer
Handles all Anki-specific functionality including the user interface, plugin lifecycle, and integration with Anki's API. This is what gets installed into Anki.

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
./scripts/deploy.sh 
```

- Restart Anki
- The plugin should appear in Tools → German Card Generator

## 🔧 Troubleshooting

### OpenAI API Quota Issues
If integration tests fail with Error code: 429 - "quota exceeded" error: you need to top up your balance at [OpenAI Platform](https://platform.openai.com/). Tests cost pennies.

### Plugin Not Appearing in Anki
- Restart Anki after deployment
- Check Tools → German Card Generator menu

### Plugin Carashes in Anki with an error `The 'openai' package is missing. Please ensure the addon was bundled correctly.`
- Install dependencies into the `plugin/vendor` folder using: `./scripts/bundle.py`

### Binary dependency errors (e.g. `No module named 'pydantic_core._pydantic_core'`). 
- Make sure to bundle dependencies using **Python 3.9** (the same version as Anki). Use `pyenv local 3.9.21` and create your venv with that version before running the bundle script. The `.so` files in `vendor` must match Anki's Python version.