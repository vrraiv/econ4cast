"""Import Bureau of Economic Analysis source data."""

from __future__ import annotations

import argparse
import os

from econ4cast.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/forecast_config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    source_config = config["sources"]["bea"]
    api_key_name = source_config.get("api_key_env")
    api_key = os.getenv(api_key_name) if api_key_name else None
    datasets = source_config.get("datasets", [])
    key_status = "available" if api_key else "missing"
    print(f"BEA import scaffold loaded {len(datasets)} configured dataset(s); API key {key_status}.")


if __name__ == "__main__":
    main()
