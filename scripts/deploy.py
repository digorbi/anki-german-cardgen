#!/usr/bin/env python3
"""
Deploy script for Anki German Card Generator Plugin (macOS only).

Usage:
  OPENAI_API_KEY=sk-... ./scripts/deploy.sh
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


def _log(message: str) -> None:
    print(message)


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _copy_glob(source_dir: Path, pattern: str, destination: Path) -> None:
    for path in source_dir.glob(pattern):
        if path.is_file():
            shutil.copy2(path, destination)


def _set_openai_key(config_path: Path, api_key: str) -> None:
    if not config_path.exists():
        return
    data = json.loads(config_path.read_text(encoding="utf-8"))
    data["openai_api_key"] = api_key
    config_path.write_text(json.dumps(data, indent=4) + "\n", encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    addon_dir = Path.home() / "Library/Application Support/Anki2/addons21/german-cardgen"

    _log("Deploying German Card Generator Plugin...")

    if addon_dir.exists():
        _log("Cleaning up existing files...")
        for entry in addon_dir.iterdir():
            if entry.is_dir():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    else:
        _log("Creating Anki add-ons directory...")
        addon_dir.mkdir(parents=True)

    (addon_dir / "core").mkdir(parents=True, exist_ok=True)

    _log("Copying core files...")
    _copy_glob(project_root / "core", "*.py", addon_dir / "core")

    _log("Copying plugin files...")
    _copy_glob(project_root / "plugin", "*.py", addon_dir)
    _copy_glob(project_root / "plugin", "*.json", addon_dir)
    _copy_glob(project_root / "plugin", "*.md", addon_dir)

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _log("Setting OpenAI API key in deployed config...")
        _set_openai_key(addon_dir / "config.json", api_key)
    else:
        _log("OPENAI_API_KEY not set; leaving config.json unchanged.")

    _log("Copying bundled dependencies...")
    _copy_tree(project_root / "plugin" / "vendor", addon_dir / "vendor")

    _log("Copying prompts directory...")
    _copy_tree(project_root / "prompts", addon_dir / "prompts")

    _log("Copying templates directory...")
    _copy_tree(project_root / "templates", addon_dir / "templates")

    _log("Plugin deployed successfully!")
    _log("Please restart Anki to load the updated plugin.")


if __name__ == "__main__":
    main()
