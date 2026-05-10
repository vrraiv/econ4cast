"""Data catalog structures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceSeries:
    """Metadata for one provider series or dataset slice."""

    provider: str
    source_id: str
    geography: str
    concept: str
    frequency: str
    units: str | None = None
    transformation: str | None = None
