import pytest
import requests

from econ4cast.api_clients import fred


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self) -> None:
        self.raise_for_status_called = True

    def json(self):
        return self.payload


def test_get_series_observations_requests_json_payload(monkeypatch) -> None:
    response = FakeResponse({"observations": [{"date": "2026-01-01", "value": "1.0"}]})
    calls = []

    def fake_get(url, *, params, timeout):
        calls.append({"url": url, "params": params, "timeout": timeout})
        return response

    monkeypatch.setattr(requests, "get", fake_get)

    payload = fred.get_series_observations(
        "test-api-key",
        "GDPC1",
        observation_start="1995-01-01",
        timeout=5,
    )

    assert payload == {"observations": [{"date": "2026-01-01", "value": "1.0"}]}
    assert response.raise_for_status_called is True
    assert calls == [
        {
            "url": "https://api.stlouisfed.org/fred/series/observations",
            "params": {
                "api_key": "test-api-key",
                "file_type": "json",
                "series_id": "GDPC1",
                "observation_start": "1995-01-01",
            },
            "timeout": 5,
        }
    ]


def test_get_series_observations_rejects_non_object_payload(monkeypatch) -> None:
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse([]))

    with pytest.raises(TypeError, match="JSON object"):
        fred.get_series_observations("test-api-key", "GDPC1")
