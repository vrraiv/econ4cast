import importlib.util
import json
from pathlib import Path

import pytest
import yaml


def _load_import_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "imports" / "import_fred.py"
    spec = importlib.util.spec_from_file_location("import_fred", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


import_fred = _load_import_module()
run_import = import_fred.run_import


def _write_config(tmp_path: Path) -> Path:
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    (sources_dir / "fred.yaml").write_text(
        yaml.safe_dump(
            {
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
        ),
        encoding="utf-8",
    )
    config_path = tmp_path / "forecast_config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "paths": {"raw_data": str(tmp_path / "raw")},
                "sources": {"fred": "sources/fred.yaml"},
                "modeling": {},
            }
        ),
        encoding="utf-8",
    )
    return config_path


def test_fred_dry_run_does_not_require_api_key(tmp_path: Path, monkeypatch, capsys) -> None:
    config_path = _write_config(tmp_path)
    monkeypatch.delenv("FRED_API_KEY", raising=False)

    exit_code = run_import(str(config_path), dry_run=True)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "not required for dry run" in captured.out
    assert "GDPC1" in captured.out


def test_fred_non_dry_run_requires_api_key(tmp_path: Path, monkeypatch) -> None:
    config_path = _write_config(tmp_path)
    monkeypatch.delenv("FRED_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="FRED_API_KEY"):
        run_import(str(config_path), dry_run=False)


def test_fred_non_dry_run_fetches_and_saves_raw_payload_without_printing_secret(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    config_path = _write_config(tmp_path)
    monkeypatch.setenv("FRED_API_KEY", "super-secret-test-key")
    calls = []

    def fake_get_series_observations(api_key: str, series_id: str, **params):
        calls.append({"api_key": api_key, "series_id": series_id, "params": params})
        return {
            "realtime_start": "2026-05-12",
            "realtime_end": "2026-05-12",
            "observation_start": "1995-01-01",
            "observations": [{"date": "1995-01-01", "value": "1.0"}],
        }

    monkeypatch.setattr(import_fred, "get_series_observations", fake_get_series_observations)

    exit_code = run_import(str(config_path), dry_run=False)

    captured = capsys.readouterr()
    raw_payload_path = tmp_path / "raw" / "fred" / "GDPC1_observations.json"
    assert exit_code == 0
    assert calls == [
        {
            "api_key": "super-secret-test-key",
            "series_id": "GDPC1",
            "params": {"observation_start": "1995-01-01"},
        }
    ]
    assert json.loads(raw_payload_path.read_text(encoding="utf-8"))["observations"] == [
        {"date": "1995-01-01", "value": "1.0"}
    ]
    assert "super-secret-test-key" not in captured.out
    assert "API key is available" in captured.out
    assert "GDPC1_observations.json" in captured.out
