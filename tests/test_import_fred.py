import importlib.util
from pathlib import Path

import pytest
import yaml


def _load_run_import():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "imports" / "import_fred.py"
    spec = importlib.util.spec_from_file_location("import_fred", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_import


run_import = _load_run_import()


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


def test_fred_non_dry_run_accepts_api_key_without_printing_secret(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    config_path = _write_config(tmp_path)
    monkeypatch.setenv("FRED_API_KEY", "super-secret-test-key")

    exit_code = run_import(str(config_path), dry_run=False)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "super-secret-test-key" not in captured.out
    assert "API key is available" in captured.out
