"""Bureau of Economic Analysis API access helpers."""

from __future__ import annotations

from typing import Any

import requests


BASE_URL = "https://apps.bea.gov/api/data"


def get_bea_data(api_key: str, **params: Any) -> dict[str, Any]:
    """Fetch data from the BEA API."""
    request_params = {
        "UserID": api_key,
        "method": "GetData",
        "ResultFormat": "JSON",
        **params,
    }
    response = requests.get(BASE_URL, params=request_params, timeout=60)
    response.raise_for_status()
    return response.json()
