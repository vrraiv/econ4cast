"""FRED API access helpers."""

from __future__ import annotations

from typing import Any

import requests


BASE_URL = "https://api.stlouisfed.org/fred"


def get_series_observations(api_key: str, series_id: str, **params: Any) -> dict[str, Any]:
    """Fetch observations for a FRED series."""
    request_params = {
        "api_key": api_key,
        "file_type": "json",
        "series_id": series_id,
        **params,
    }
    response = requests.get(f"{BASE_URL}/series/observations", params=request_params, timeout=60)
    response.raise_for_status()
    return response.json()
