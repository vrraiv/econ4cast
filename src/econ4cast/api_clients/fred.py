"""FRED API access helpers."""

from __future__ import annotations

from typing import Any

import requests


BASE_URL = "https://api.stlouisfed.org/fred"


def get_series_observations(
    api_key: str,
    series_id: str,
    *,
    observation_start: str | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Fetch raw observation data for a FRED series.

    The returned mapping is the provider-shaped JSON response from FRED's
    ``series/observations`` endpoint. This helper intentionally does not
    normalize observations or attach project-specific metadata.
    """
    request_params = {
        "api_key": api_key,
        "file_type": "json",
        "series_id": series_id,
    }
    if observation_start is not None:
        request_params["observation_start"] = observation_start

    response = requests.get(
        f"{BASE_URL}/series/observations",
        params=request_params,
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError(f"Expected FRED observations response for {series_id} to be a JSON object.")
    return payload
