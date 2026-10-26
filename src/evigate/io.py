"""Safe read-only loading for EviGate validation records."""

import json
from pathlib import Path
from typing import Any

import yaml


def _load_value(path: Path) -> Any:
    """Load one JSON or YAML value without modifying the source file."""

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        value = yaml.safe_load(text)
    else:
        value = json.loads(text)
    return value


def load_mapping(path: Path) -> dict[str, Any]:
    """Load a JSON or YAML mapping without modifying the source file."""

    value = _load_value(path)
    if not isinstance(value, dict):
        raise ValueError("Record must contain a mapping object.")
    return value


def load_list(path: Path) -> list[dict[str, Any]]:
    """Load a JSON or YAML list of mapping records without writing it."""

    value = _load_value(path)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("Record must contain a list of mapping objects.")
    return value
