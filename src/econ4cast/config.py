"""Configuration loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path = "config/forecast_config.yaml") -> dict[str, Any]:
    """Load the top-level YAML configuration and referenced module files."""
    config_path = Path(path)
    config = _load_yaml(config_path)
    base_dir = config_path.parent

    _resolve_named_modules(config, "sources", base_dir)
    _resolve_named_modules(config, "targets", base_dir)
    _resolve_single_module(config, "transforms", base_dir)
    _add_compatibility_aliases(config)

    return config


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
