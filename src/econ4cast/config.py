"""Configuration loading and validation helpers."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import yaml


FRED_FREQUENCIES = {"daily", "weekly", "monthly", "quarterly", "annual"}
FRED_TOP_LEVEL_FIELDS = {"enabled", "raw_subdir", "api_key_env", "series"}
FRED_FORBIDDEN_SECRET_FIELDS = {"api_key", "api_key_value", "key", "token", "access_token"}
FRED_REQUIRED_SERIES_FIELDS = {
    "series_id",
    "name",
    "geography",
    "frequency",
    "units",
    "seasonal_adjustment",
}
FRED_OPTIONAL_SERIES_FIELDS = {"observation_start", "transformations"}
FRED_SERIES_FIELDS = FRED_REQUIRED_SERIES_FIELDS | FRED_OPTIONAL_SERIES_FIELDS


def load_config(path: str | Path = "config/forecast_config.yaml") -> dict[str, Any]:
    """Load the top-level YAML configuration and referenced module files."""
    config_path = Path(path)
    config = _load_yaml(config_path)
    base_dir = config_path.parent

    _resolve_named_modules(config, "sources", base_dir)
    _resolve_named_modules(config, "targets", base_dir)
    _resolve_single_module(config, "transforms", base_dir)
    _validate_loaded_config(config)
    _add_compatibility_aliases(config)

    return config


def validate_fred_source_config(source_config: dict[str, Any], label: str = "FRED source config") -> None:
    """Validate the repository's FRED source configuration contract.

    The contract intentionally covers metadata and importer control fields only.
    It does not require an API key value because secrets must be supplied through
    the environment at runtime.
    """
    if not isinstance(source_config, dict):
        raise TypeError(f"{label} must be a mapping.")

    extra_fields = sorted(set(source_config) - FRED_TOP_LEVEL_FIELDS)
    forbidden_fields = sorted(FRED_FORBIDDEN_SECRET_FIELDS & set(source_config))
    if forbidden_fields:
        fields = ", ".join(forbidden_fields)
        raise ValueError(
            f"{label} must not contain hardcoded secret field(s): {fields}. "
            "Use 'api_key_env' to name the runtime environment variable."
        )
    if extra_fields:
        fields = ", ".join(extra_fields)
        allowed = ", ".join(sorted(FRED_TOP_LEVEL_FIELDS))
        raise ValueError(f"{label} contains unknown top-level field(s): {fields}. Allowed fields: {allowed}.")

    enabled = source_config.get("enabled")
    if not isinstance(enabled, bool):
        raise TypeError(f"{label} field 'enabled' must be a boolean.")

    raw_subdir = source_config.get("raw_subdir")
    if not _is_non_empty_string(raw_subdir):
        raise ValueError(f"{label} field 'raw_subdir' must be a non-empty string.")

    api_key_env = source_config.get("api_key_env")
    if not _is_non_empty_string(api_key_env):
        raise ValueError(f"{label} field 'api_key_env' must name the environment variable.")

    series = source_config.get("series")
    if not isinstance(series, list):
        raise TypeError(f"{label} field 'series' must be a list.")

    for index, series_config in enumerate(series):
        _validate_fred_series_config(series_config, f"{label} series[{index}]")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    if not isinstance(config, dict):
        raise TypeError(f"Expected mapping configuration in {path}.")
    return config


def _resolve_named_modules(config: dict[str, Any], key: str, base_dir: Path) -> None:
    modules = config.get(key)
    if not isinstance(modules, dict):
        return

    config[key] = {
        name: _load_yaml(base_dir / module_path) if isinstance(module_path, str) else module_path
        for name, module_path in modules.items()
    }


def _resolve_single_module(config: dict[str, Any], key: str, base_dir: Path) -> None:
    module_path = config.get(key)
    if isinstance(module_path, str):
        config[key] = _load_yaml(base_dir / module_path)


def _validate_loaded_config(config: dict[str, Any]) -> None:
    sources = config.get("sources")
    if not isinstance(sources, dict) or "fred" not in sources:
        return
    validate_fred_source_config(sources["fred"])


def _validate_fred_series_config(series_config: Any, label: str) -> None:
    if not isinstance(series_config, dict):
        raise TypeError(f"{label} must be a mapping.")

    extra_fields = sorted(set(series_config) - FRED_SERIES_FIELDS)
    forbidden_fields = sorted(FRED_FORBIDDEN_SECRET_FIELDS & set(series_config))
    if forbidden_fields:
        fields = ", ".join(forbidden_fields)
        raise ValueError(
            f"{label} must not contain hardcoded secret field(s): {fields}. "
            "Series entries must only contain request metadata."
        )
    if extra_fields:
        fields = ", ".join(extra_fields)
        allowed = ", ".join(sorted(FRED_SERIES_FIELDS))
        raise ValueError(f"{label} contains unknown field(s): {fields}. Allowed fields: {allowed}.")

    missing_fields = sorted(FRED_REQUIRED_SERIES_FIELDS - set(series_config))
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ValueError(f"{label} is missing required field(s): {missing}.")

    for field in sorted(FRED_REQUIRED_SERIES_FIELDS):
        if not _is_non_empty_string(series_config.get(field)):
            raise ValueError(f"{label} field '{field}' must be a non-empty string.")

    frequency = series_config["frequency"]
    if frequency not in FRED_FREQUENCIES:
        allowed = ", ".join(sorted(FRED_FREQUENCIES))
        raise ValueError(f"{label} field 'frequency' must be one of: {allowed}.")

    observation_start = series_config.get("observation_start")
    if observation_start is not None and not _is_yyyy_mm_dd_date(observation_start):
        raise ValueError(f"{label} field 'observation_start' must be a YYYY-MM-DD date string.")

    transformations = series_config.get("transformations", [])
    if not isinstance(transformations, list) or not all(
        _is_non_empty_string(transformation) for transformation in transformations
    ):
        raise TypeError(f"{label} field 'transformations' must be a list of non-empty strings.")


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_yyyy_mm_dd_date(value: Any) -> bool:
    if not _is_non_empty_string(value):
        return False
    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        return False
    return value == parsed_date.isoformat()


def _add_compatibility_aliases(config: dict[str, Any]) -> None:
    if "sources" in config and "api_sources" not in config:
        config["api_sources"] = config["sources"]

    modeling = config.get("modeling")
    transforms = config.get("transforms")
    if not isinstance(modeling, dict) or not isinstance(transforms, dict):
        return

    target_concepts = transforms.get("target_concepts")
    if "targets" not in modeling and isinstance(target_concepts, list):
        modeling["targets"] = target_concepts

    defaults = transforms.get("defaults")
    if "transformations" not in modeling and isinstance(defaults, dict):
        transformations = {}
        if "growth_rate" in defaults:
            transformations["default_growth_rate"] = defaults["growth_rate"]
        if "inflation_rate" in defaults:
            transformations["default_inflation_rate"] = defaults["inflation_rate"]
        if transformations:
            modeling["transformations"] = transformations
