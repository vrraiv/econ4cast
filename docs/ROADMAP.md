# Roadmap

## Phase 1: Source Catalog

- Select first forecasting targets for each economy.
- Record provider table IDs, series IDs, geographies, frequencies, units,
  transformations, and release calendar assumptions.
- Fill `config/forecast_config.yaml` with the selected source series.

## Phase 2: Reproducible Ingestion

- Implement complete provider requests for StatCan, BEA, FRED, and Eurostat.
- Store raw API payloads under `data/raw/<provider>/`.
- Add lightweight validation that confirms expected fields, date ranges, and
  observation counts.

## Phase 3: Harmonized Panels

- Convert raw provider payloads into cleaned interim extracts.
- Build cross-economy merged panels with consistent dates, units, frequencies,
  and concept names.
- Document transformation choices that affect comparability.

## Phase 4: Forecasting Models

- Establish random walk and AR(1) benchmark runs for each target.
- Add nowcasting and medium-term forecasting models once the merged panels are
  stable.
- Keep reusable model logic in `src/econ4cast/forecasting/`.

## Phase 5: Evaluation and Reporting

- Define evaluation windows, forecast horizons, metrics, and vintage handling.
- Compare model forecasts against naive benchmarks.
- Produce reproducible tables, plots, and notebooks for diagnostics and
  communication.
