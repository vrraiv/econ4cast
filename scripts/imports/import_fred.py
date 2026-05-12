"""Import raw FRED source data payloads."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from econ4cast.api_clients.base import write_json  # noqa: E402
from econ4cast.api_clients.fred import get_series_observations  # noqa: E402
from econ4cast.config import load_config, validate_fred_source_config  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    """Build the FRED importer command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/forecast_config.yaml")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the FRED config and report planned requests without requiring a key.",
    )
    return parser


def run_import(config_path: str, *, dry_run: bool = False) -> int:
    """Run FRED raw import orchestration."""
    config = load_config(config_path)
    source_config = config["sources"]["fred"]
    validate_fred_source_config(source_config)

    api_key_name = source_config["api_key_env"]
    api_key = os.getenv(api_key_name)
    series = source_config["series"]
    enabled = source_config["enabled"]

    if not enabled:
        print("FRED import disabled by config; no requests planned.")
        return 0

    if dry_run:
        print(
            "FRED dry run validated "
            f"{len(series)} configured series; API key env {api_key_name}; "
            f"API key {'available' if api_key else 'not required for dry run'}."
        )
        for series_config in series:
            print(_format_planned_series(series_config))
        return 0

    if not api_key:
        raise RuntimeError(
            f"FRED API key is required for non-dry-run imports. Set {api_key_name} in the environment."
        )

    raw_dir = _raw_output_dir(config, source_config)
    print(f"FRED config validated and API key is available; importing {len(series)} series.")
    for series_config in series:
        series_id = series_config["series_id"]
        payload = get_series_observations(
            api_key,
            series_id,
            observation_start=series_config.get("observation_start"),
        )
        output_path = _raw_output_path(raw_dir, series_id)
        write_json(payload, output_path)
        print(f"Saved raw FRED response for {series_id} to {output_path}.")

    return 0


def _format_planned_series(series_config: dict[str, Any]) -> str:
    series_id = series_config["series_id"]
    frequency = series_config["frequency"]
    observation_start = series_config.get("observation_start", "provider default")
    return f"Would request FRED series {series_id} ({frequency}) from {observation_start}."


def _raw_output_dir(config: dict[str, Any], source_config: dict[str, Any]) -> Path:
    paths_config = config.get("paths", {})
    raw_data_dir = (
        paths_config.get("raw_data", "data/raw")
        if isinstance(paths_config, dict)
        else "data/raw"
    )
    return Path(raw_data_dir) / source_config["raw_subdir"]


def _raw_output_path(raw_dir: Path, series_id: str) -> Path:
    safe_series_id = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in series_id
    )
    return raw_dir / f"{safe_series_id}_observations.json"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_import(args.config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
