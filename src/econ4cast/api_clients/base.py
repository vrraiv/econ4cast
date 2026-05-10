"""Shared helpers for API clients."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(payload: dict[str, Any] | list[Any], path: str | Path) -> Path:
    """Write an API payload to disk as formatted JSON."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)
    return output_path
