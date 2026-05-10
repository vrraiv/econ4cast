"""Eurostat API access helpers."""

from __future__ import annotations

from typing import Any

import requests


BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"


def get_dataset(dataset_id: str, **params: Any) -> dict[str, Any]:
    """Fetch a Eurostat dataset as JSON."""
    response = requests.get(f"{BASE_URL}/{dataset_id}", params=params, timeout=60)
    response.raise_for_status()
    return response.json()
