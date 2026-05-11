import pytest

from econ4cast.config import validate_fred_source_config


def _valid_fred_config() -> dict:
    return {
        "enabled": True,
        "raw_subdir": "fred",
        "api_key_env": "FRED_API_KEY",
        "series": [
            {
                "series_id": "GDPC1",
                "name": "Real Gross Domestic Product",
                "geography": "us",
                "frequency": "quarterly",
                "units": "Billions of chained dollars",
                "seasonal_adjustment": "seasonally_adjusted_annual_rate",
                "observation_start": "1995-01-01",
                "transformations": ["annualized_qoq_growth"],
            }
        ],
    }


def test_validate_fred_source_config_accepts_contract() -> None:
    validate_fred_source_config(_valid_fred_config())


@pytest.mark.parametrize(
    "api_key_env",
    ["", "fred_api_key", "FRED-API-KEY", "1FRED_API_KEY", "abc123literalkey"],
)
def test_validate_fred_source_config_requires_api_key_env_name(api_key_env: str) -> None:
    config = _valid_fred_config()
    config["api_key_env"] = api_key_env

    with pytest.raises(ValueError, match="api_key_env"):
        validate_fred_source_config(config)


def test_validate_fred_source_config_requires_series_metadata() -> None:
    config = _valid_fred_config()
    del config["series"][0]["units"]

    with pytest.raises(ValueError, match="units"):
        validate_fred_source_config(config)


def test_validate_fred_source_config_rejects_unknown_frequency() -> None:
    config = _valid_fred_config()
    config["series"][0]["frequency"] = "fortnightly"

    with pytest.raises(ValueError, match="frequency"):
        validate_fred_source_config(config)


def test_validate_fred_source_config_rejects_hardcoded_api_key_field() -> None:
    config = _valid_fred_config()
    config["api_key"] = "not-a-real-key"

    with pytest.raises(ValueError, match="hardcoded secret"):
        validate_fred_source_config(config)


def test_validate_fred_source_config_rejects_unknown_top_level_fields() -> None:
    config = _valid_fred_config()
    config["unexpected"] = "value"

    with pytest.raises(ValueError, match="unknown top-level field"):
        validate_fred_source_config(config)


@pytest.mark.parametrize(
    "observation_start",
    ["1995", "1995/01/01", "yesterday", "2024-2-03", "2024-02-30"],
)
def test_validate_fred_source_config_rejects_malformed_observation_start(observation_start: str) -> None:
    config = _valid_fred_config()
    config["series"][0]["observation_start"] = observation_start

    with pytest.raises(ValueError, match="observation_start"):
        validate_fred_source_config(config)
