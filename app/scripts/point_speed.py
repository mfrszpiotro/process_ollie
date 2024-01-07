import numpy as np
import pandas as pd
from scipy import signal


def get_point_speed(
    colx: pd.Series, coly: pd.Series, colz: pd.Series, time: pd.Series
) -> pd.Series:
    p1 = np.array([colx, coly, colz])
    p2 = np.array([colx.shift(1), coly.shift(1), colz.shift(1)])
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)

    return dist / time


def add_and_plot(df: pd.DataFrame, point_name: str):
    df[f"{point_name}_speed"] = get_point_speed(
        df[f"{point_name}_x"], df[f"{point_name}_y"], df[f"{point_name}_z"], df.Time
    )
    df[f"{point_name}_speed_smooth"] = signal.savgol_filter(
        df[f"{point_name}_speed"], window_length=6, polyorder=3, mode="nearest"
    )
    ax_foot = df.plot(
        kind="line",
        x="Time",
        y=f"{point_name}_speed_smooth",
        label="Smoothened foot speed [unit/s]",
    )
    df.plot(
        kind="line",
        x="Time",
        y=f"{point_name}_speed",
        label=f"{point_name} speed [unit/s]",
        title=f"{point_name} speed over time while performing Ollie",
        ax=ax_foot,
    )
