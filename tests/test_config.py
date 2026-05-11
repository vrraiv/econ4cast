from pathlib import Path

from econ4cast.config import load_config


def test_load_config_resolves_modular_files() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_config(repo_root / "config" / "forecast_config.yaml")

    assert config["sources"]["fred"]["api_key_env"] == "FRED_API_KEY"
    assert config["sources"]["bea"]["raw_subdir"] == "bea"
    assert config["targets"]["us_gdp"]["primary_source"] == "bea"
    assert config["targets"]["canada_gdp"]["primary_source"] == "statcan"
    assert config["targets"]["eurozone_gdp"]["primary_source"] == "eurostat"
    assert config["transforms"]["defaults"]["growth_rate"] == "annualized_qoq"
    assert config["api_sources"] is config["sources"]
    assert config["modeling"]["targets"] == [
        "real_gdp_growth",
        "inflation",
        "unemployment_rate",
    ]
    assert config["modeling"]["transformations"]["default_growth_rate"] == "annualized_qoq"
