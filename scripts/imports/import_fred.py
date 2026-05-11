"""Validate and dry-run FRED source data imports."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

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
    """Run FRED import orchestration.

    The current issue scope is limited to configuration validation and dry-run
    behavior. Non-dry-run execution checks that the configured API key is present
    but intentionally does not download provider data yet.
    """
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

    print(
        "FRED config validated and API key is available; "
        "data download is intentionally not implemented in this config-contract change."
    )
    return 0


def _format_planned_series(series_config: dict[str, Any]) -> str:
    series_id = series_config["series_id"]
    frequency = series_config["frequency"]
    observation_start = series_config.get("observation_start", "provider default")
    return f"Would request FRED series {series_id} ({frequency}) from {observation_start}."


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_import(args.config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
