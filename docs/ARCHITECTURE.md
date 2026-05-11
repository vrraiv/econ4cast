# Architecture

`econ4cast` is a Python package and project workspace for short- and
medium-term macroeconomic forecasting across the United States, Canada, and the
eurozone.

## Repository Layout

```text
econ4cast/
  AGENTS.md
  README.md
  pyproject.toml
  config/
    forecast_config.yaml
    transforms.yaml
    sources/
      fred.yaml
      bea.yaml
      statcan.yaml
      eurostat.yaml
    targets/
      us_gdp.yaml
      canada_gdp.yaml
      eurozone_gdp.yaml
  data/
    raw/
    interim/
    merged/
    processed/
  docs/
    ARCHITECTURE.md
    DECISIONS.md
    HANDOFF.md
    OPEN_QUESTIONS.md
    ROADMAP.md
  notebooks/
  scripts/
    imports/
  src/
    econ4cast/
      api_clients/
      data/
      forecasting/
      visualization/
  tests/
```

## Main Components

- `config/forecast_config.yaml`: Top-level run, calendar, geography, modeling,
  output, and config module orchestration.
- `config/sources/`: Provider-specific source catalogs for StatCan, BEA, FRED,
  and Eurostat.
- `config/targets/`: Economy-specific forecasting target definitions.
- `config/transforms.yaml`: Shared transformation defaults and target concept
  names.
- `scripts/imports/`: Provider-specific command-line import scaffolds. These
  scripts read configuration, check required environment variables, and should
  orchestrate provider clients.
- `src/econ4cast/api_clients/`: Reusable API access helpers for StatCan, BEA,
  FRED, and Eurostat. Provider modules should return provider-shaped payloads;
  persistence belongs in orchestration or shared helpers.
- `src/econ4cast/data/`: Data catalog and path helpers used by ingestion,
  harmonization, and modeling code.
- `src/econ4cast/forecasting/`: Forecast benchmarks and evaluation helpers.
  Current baseline models include random walk and AR(1).
- `src/econ4cast/visualization/`: Reusable plotting helpers for validation,
  diagnostics, and communication.
- `data/raw/`: Direct provider payloads, organized by provider. Raw downloaded
  data is not committed.
- `data/interim/`, `data/merged/`, `data/processed/`: Cleaned provider extracts,
  cross-economy panels, and final modeling or forecast outputs.

## Data Flow

1. Define source series, provider identifiers, geography, frequency, units, and
   transformations in the modular files referenced by
   `config/forecast_config.yaml`.
2. Run provider import scripts in `scripts/imports/`.
3. Store direct API payloads under `data/raw/<provider>/`.
4. Build provider-specific cleaned extracts in `data/interim/`.
5. Harmonize concepts, dates, geography labels, frequencies, and units into
   `data/merged/`.
6. Produce final model panels, forecasts, evaluation tables, and artifacts under
   `data/processed/`.

## Boundaries

- Reusable code belongs in `src/econ4cast/`.
- One-off orchestration and CLI entry points belong in `scripts/`.
- Exploratory analysis, diagnostics, and presentation work belongs in
  `notebooks/` until reusable logic is moved into the package.
- Architectural changes should be recorded in `docs/DECISIONS.md` and reflected
  here when they change the repository or application structure.
