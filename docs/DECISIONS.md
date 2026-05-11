# Decisions

Record architectural and methodological choices here when they affect project
structure, data reproducibility, modeling contracts, or cross-economy
comparability.

## Accepted

### Use a `src/` Python Package Layout

- Date: 2026-05-11
- Decision: Reusable code lives under `src/econ4cast/`; orchestration scripts
  live under `scripts/`.
- Rationale: This keeps importable library code separate from one-off commands
  and notebook exploration.

### Preserve Raw Provider Payloads

- Date: 2026-05-11
- Decision: Direct API responses belong under `data/raw/<provider>/` and should
  not be hand-edited.
- Rationale: Forecast datasets must be reproducible from documented provider
  sources and transformations.

### Keep Provider Access Modular

- Date: 2026-05-11
- Decision: StatCan, BEA, FRED, and Eurostat access helpers live in separate
  modules under `src/econ4cast/api_clients/`.
- Rationale: Provider APIs have different authentication, request, and response
  shapes, while higher-level ingestion can share orchestration patterns.

### Track Naive Benchmarks First

- Date: 2026-05-11
- Decision: Random walk and AR(1) benchmarks are the initial forecast baselines.
- Rationale: More complex nowcasting and medium-term models need simple,
  reproducible comparisons before they can be evaluated credibly.

### Split Configuration Into Modular Catalogs

- Date: 2026-05-11
- Decision: Keep `config/forecast_config.yaml` as the top-level orchestration
  file and split provider sources, forecast targets, and shared transformations
  into `config/sources/`, `config/targets/`, and `config/transforms.yaml`.
- Rationale: Source metadata, target definitions, and transformation defaults
  will grow at different rates, so separate files keep updates reviewable while
  preserving one config entry point for scripts.

## Proposed

- Define a stable schema for source catalog entries and merged panel columns.
- Decide how to represent vintages and release calendars.
- Decide whether forecast artifacts are file-based outputs, database tables, or
  both.

### Validate the FRED Source Contract Before Import

- Date: 2026-05-11
- Decision: `config/sources/fred.yaml` must define runtime key lookup metadata
  and a validated per-series metadata contract before FRED import orchestration
  can run.
- Rationale: The first provider-specific config contract should prevent
  malformed source entries and keep API keys in environment variables rather
  than committed YAML files.
