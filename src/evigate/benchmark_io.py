"""Safe local I/O helpers for benchmark artifacts."""

import json
from pathlib import Path
from typing import Any


def write_new_json(path: Path, record: dict[str, Any]) -> None:
    """Write a new JSON artifact and refuse to overwrite an existing one."""

    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
