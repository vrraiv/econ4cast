# Open Questions

Use this file to track unresolved project questions that affect implementation,
data definitions, or modeling decisions.

## Data Sources

- Which exact provider series or tables should be used for real GDP growth,
  inflation, and unemployment in each economy?
- What source should define eurozone aggregate concepts when Eurostat offers
  multiple related datasets?
- Which source metadata must be stored alongside each raw payload?

## Transformation and Harmonization

- Should growth rates be stored as provider-reported values, derived values, or
  both?
- What is the canonical date representation for monthly and quarterly series?
- How should mixed-frequency inputs be aligned for nowcasting models?
- Which units, seasonal adjustment flags, and price bases are required in merged
  panels?

## Vintages and Releases

- Will the project track historical data vintages, latest available data only,
  or both?
- How should release calendar assumptions be represented in configuration?
- What is the policy for revisions when providers update historical observations?

## Forecasting and Evaluation

- Which forecast horizons should be reported for each target?
- What evaluation windows are required before comparing model performance?
- Which models should be added after the random walk and AR(1) benchmarks?
- What forecast artifact format should downstream notebooks and reports consume?
