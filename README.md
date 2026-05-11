# econ4cast

Python libraries, scripts, and notebooks for short- and medium-term forecasts
for the United States, Canada, and the eurozone.

## Project Structure

```text
econ4cast/
  AGENTS.md
  README.md
  pyproject.toml
  config/
    forecast_config.yaml
    transforms.yaml
    sources/
      bea.yaml
      eurostat.yaml
      fred.yaml
      statcan.yaml
    targets/
      canada_gdp.yaml
      eurozone_gdp.yaml
      us_gdp.yaml
  data/
    raw/
      statcan/
      bea/
      fred/
      eurostat/
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
      import_bea.py
      import_eurostat.py
      import_fred.py
      import_statcan.py
  src/
    econ4cast/
      api_clients/
      data/
      forecasting/
      visualization/
  tests/
```

## Workflow

1. Define the dataset using StatCan, BEA, Eurostat, and FRED API services and
   documentation. Record source table IDs, series IDs, geography, frequency,
   transformations, and release calendar assumptions in `config/`.
2. Import and visualize all data. Store source downloads in `data/raw/<provider>/`
   and keep reusable ingestion logic in `src/econ4cast/api_clients/`.
3. Design nowcasting and medium-term forecasting models using time series
   econometrics. Put reusable model code in `src/econ4cast/forecasting/` and use
   notebooks for model diagnostics and communication.
4. Evaluate forecasts against naive benchmarks such as an AR(1) model or a
   random walk. Track evaluation windows, target vintages, forecast horizons, and
   metrics in configuration or structured outputs.

## Data Layout

- `data/raw/`: Direct API responses or provider-shaped files. These files are not
  committed to git.
- `data/interim/`: Cleaned provider-specific extracts.
- `data/merged/`: Cross-economy comparison datasets with harmonized concepts,
  dates, and units.
- `data/processed/`: Final modeling datasets and evaluation panels.

## API Client Layout

Provider-specific client modules live in `src/econ4cast/api_clients/`:

- `statcan.py`: Statistics Canada data access helpers.
- `bea.py`: Bureau of Economic Analysis data access helpers.
- `fred.py`: Federal Reserve Economic Data helpers.
- `eurostat.py`: Eurostat data access helpers.

Command-line ingestion entry points live in `scripts/imports/`.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and fill in optional API keys for services that
require them.

## First Commands

```powershell
python scripts/imports/import_fred.py --config config/forecast_config.yaml --dry-run
python scripts/imports/import_bea.py --config config/forecast_config.yaml
python scripts/imports/import_statcan.py --config config/forecast_config.yaml
python scripts/imports/import_eurostat.py --config config/forecast_config.yaml
```

The FRED importer currently supports a config-validation dry run. A non-dry-run
FRED import requires `FRED_API_KEY` in the environment, validates that it is
present, and intentionally stops before downloading data while the source
catalog is still being defined.

## FRED Source Configuration

`config/sources/fred.yaml` defines the repository contract for FRED metadata and
runtime key lookup. Keep real API keys out of the file; set `FRED_API_KEY` in
the environment or in an uncommitted `.env` file instead. Each configured FRED
series must include:

- `series_id`: FRED series identifier, for example `GDPC1`.
- `name`: Human-readable label.
- `geography`: Internal geography key such as `us`.
- `frequency`: One of `daily`, `weekly`, `monthly`, `quarterly`, or `annual`.
- `units`: Provider-reported or intended request units.
- `seasonal_adjustment`: Seasonal adjustment metadata from FRED.
- `observation_start`: Optional `YYYY-MM-DD` request lower bound.
- `transformations`: Optional downstream transformation labels.

The remaining import scripts are intentionally light scaffolds. The next step is
to fill the source catalog in `config/sources/` and target catalog in
`config/targets/` with the exact API datasets, series IDs, and transformations
needed for the first forecasting targets.
