# Handoff

## Current State

- The repository is an initial scaffold for macroeconomic forecasting across the
  United States, Canada, and the eurozone.
- Provider API helper modules exist for StatCan, BEA, FRED, and Eurostat.
- Import scripts currently load configuration and report scaffold status; full
  provider ingestion still needs implementation.
- Forecasting helpers currently include random walk and AR(1) benchmarks plus
  MAE and RMSE evaluation metrics.
- `config/forecast_config.yaml` defines run metadata, geographies, data paths,
  model settings, outputs, and the modular config files to load.
- Provider settings now live under `config/sources/`, GDP target scaffolds live
  under `config/targets/`, and shared transformation defaults live in
  `config/transforms.yaml`.
- FRED now has a validated source config contract and a dry-run importer path
  that reports planned requests without requiring or printing an API key.

## Recent Work

- Added the documentation layout:
  - `docs/ARCHITECTURE.md`
  - `docs/ROADMAP.md`
  - `docs/DECISIONS.md`
  - `docs/HANDOFF.md`
  - `docs/OPEN_QUESTIONS.md`
- Added documentation upkeep rules to `AGENTS.md`.
- Updated the README project structure to include the docs layout.
- Split configuration into a top-level orchestration file plus modular source,
  target, and transform YAML files.
- Added FRED config-contract validation, dry-run importer behavior, and focused
  tests for malformed FRED config and API-key handling.

## Next Best Steps

1. Choose the first target and source series for each economy.
2. Fill provider series and dataset metadata in `config/sources/`.
3. Implement the FRED download path after the source catalog contains approved
   series; preserve raw payloads under `data/raw/fred/`.
4. Promote the first cleaned provider extract into `data/interim/`.
5. Define the merged panel schema before building cross-economy joins.

## Working Notes

- Do not commit downloaded data, API keys, model artifacts, virtual
  environments, or notebook checkpoints.
- Update this file after meaningful implementation work so the next agent can
  resume from the current project state.
