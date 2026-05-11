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


def test_validate_fred_source_config_requires_api_key_env_name() -> None:
    config = _valid_fred_config()
    config["api_key_env"] = ""

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
