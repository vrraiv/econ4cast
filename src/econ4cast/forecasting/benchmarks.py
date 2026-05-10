"""Naive forecast benchmark models."""

from __future__ import annotations

import pandas as pd
from statsmodels.tsa.ar_model import AutoReg


def random_walk_forecast(series: pd.Series, steps: int) -> pd.Series:
    """Forecast future values by carrying forward the latest observed value."""
    clean = series.dropna()
    if clean.empty:
        raise ValueError("series must contain at least one non-missing observation")
    last_value = clean.iloc[-1]
    return pd.Series([last_value] * steps, name=f"{series.name}_random_walk")


def ar1_forecast(series: pd.Series, steps: int) -> pd.Series:
    """Estimate an AR(1) model and forecast the requested number of steps."""
    clean = series.dropna()
    if len(clean) < 3:
        raise ValueError("series must contain at least three non-missing observations")
    model = AutoReg(clean, lags=1, old_names=False).fit()
    forecast = model.forecast(steps=steps)
    forecast.name = f"{series.name}_ar1"
    return forecast
