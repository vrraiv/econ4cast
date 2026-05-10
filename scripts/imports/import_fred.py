"""Import FRED source data."""

from __future__ import annotations

import argparse
import os

from econ4cast.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/forecast_config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    source_config = config["api_sources"]["fred"]
    api_key_name = source_config.get("api_key_env")
    api_key = os.getenv(api_key_name) if api_key_name else None
    series = source_config.get("series", [])
    key_status = "available" if api_key else "missing"
    print(f"FRED import scaffold loaded {len(series)} configured series; API key {key_status}.")


if __name__ == "__main__":
    main()
