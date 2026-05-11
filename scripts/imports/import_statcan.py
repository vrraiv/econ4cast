"""Import Statistics Canada source data."""

from __future__ import annotations

import argparse

from econ4cast.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/forecast_config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    datasets = config["sources"]["statcan"].get("datasets", [])
    print(f"StatCan import scaffold loaded {len(datasets)} configured dataset(s).")


if __name__ == "__main__":
    main()
