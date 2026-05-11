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

## Proposed

- Define a stable schema for source catalog entries and merged panel columns.
- Decide how to represent vintages and release calendars.
- Decide whether forecast artifacts are file-based outputs, database tables, or
  both.
