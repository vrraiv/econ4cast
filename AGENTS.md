# Repository Instructions

This repository supports short- and medium-term macroeconomic forecasting for the
United States, Canada, and the eurozone.

Before making changes, read:  

- docs/ARCHITECTURE.md  
- docs/ROADMAP.md  
- docs/DECISIONS.md  
- docs/OPEN_QUESTIONS.md

## Working Principles

- Keep source data reproducible. Store downloaded API payloads under `data/raw/`
  by provider and do not hand-edit them.
- Put cross-economy joins, harmonization, and derived datasets under
  `data/merged/`, `data/interim/`, or `data/processed/` depending on maturity.
- Keep reusable Python code in `src/econ4cast/`; keep one-off orchestration and
  ingestion commands in `scripts/`.
- Use notebooks for exploration, diagnostics, and communication. Move reusable
  logic from notebooks into the package.
- Do not commit API keys, local credentials, downloaded datasets, virtual
  environments, model artifacts, or notebook checkpoints.
- After meaningful implementation work, update `docs/HANDOFF.md`.
- After architectural choices, update `docs/DECISIONS.md`.
- If the current task changes the structure of the app, update
  `docs/ARCHITECTURE.md`.
- Prefer small, reviewable changes.  
- Do not introduce new dependencies without explaining why.  
- Preserve current architecture unless the task explicitly asks for a refactor.  
- Update docs/DECISIONS.md when making an architectural decision.  
- Update docs/HANDOFF.md after major changes.  
- When uncertain, inspect the codebase before proposing changes.

## Expected Workflow

1. Define data series and metadata using provider documentation for StatCan, BEA,
   Eurostat, and FRED.
2. Import raw data through provider-specific scripts and API client modules.
3. Visualize and validate the data before building merged cross-economy panels.
4. Estimate nowcasting and medium-term forecasting models.
5. Compare model forecasts against naive benchmarks such as random walk and AR(1)
   models.

## Planning Expectations

For non-trivial changes:  

1. Summarize relevant existing architecture.  
2. Identify affected files.  
3. Propose the smallest safe implementation path.  
4. Make changes only after the plan is clear.

## Conventions

- Configuration lives in `config/`.
- Provider clients live in `src/econ4cast/api_clients/`.
- Import scripts live in `scripts/imports/`.
- Forecasting models and benchmarks live in `src/econ4cast/forecasting/`.
- Use environment variables for secrets, for example `BEA_API_KEY` or
  `FRED_API_KEY`.
