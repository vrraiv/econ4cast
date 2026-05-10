"""Statistics Canada API access helpers."""

from __future__ import annotations

from typing import Any

import requests


BASE_URL = "https://www150.statcan.gc.ca/n1/wds/en/grp/wds"


def fetch_table_vector_data(vector_ids: list[str]) -> dict[str, Any]:
    """Fetch StatCan vector data for the requested vector IDs."""
    raise NotImplementedError("Add StatCan request payloads once source vectors are defined.")


def get(url: str, **params: Any) -> dict[str, Any]:
    """Issue a basic GET request and return JSON."""
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()
