"""Project path helpers."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def project_path(*parts: str) -> Path:
    """Return a path relative to the repository root."""
    return PROJECT_ROOT.joinpath(*parts)
