"""Forecast evaluation metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def mean_absolute_error(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate mean absolute forecast error."""
    aligned = pd.concat([actual, forecast], axis=1).dropna()
    return float((aligned.iloc[:, 0] - aligned.iloc[:, 1]).abs().mean())


def root_mean_squared_error(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate root mean squared forecast error."""
    aligned = pd.concat([actual, forecast], axis=1).dropna()
    return float(np.sqrt(((aligned.iloc[:, 0] - aligned.iloc[:, 1]) ** 2).mean()))
