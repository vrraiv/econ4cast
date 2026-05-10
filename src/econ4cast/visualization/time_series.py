"""Time series plotting helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_series(series: pd.Series, title: str | None = None) -> plt.Axes:
    """Plot one time series and return the Matplotlib axes."""
    ax = series.plot(title=title)
    ax.set_xlabel("Date")
    return ax
