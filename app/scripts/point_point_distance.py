import numpy as np
import pandas as pd
from scipy import signal


def get_point_point_distance(
    colx_a: pd.Series,
    coly_a: pd.Series,
    colz_a: pd.Series,
    colx_b: pd.Series,
    coly_b: pd.Series,
    colz_b: pd.Series,
) -> pd.Series:
    p1 = np.array([colx_a, coly_a, colz_a])
    p2 = np.array([colx_b, coly_b, colz_b])
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    return np.sqrt(squared_dist)


def add_and_plot(df: pd.DataFrame, point_name_a="FootLeft", point_name_b="FootRight"):
    df[f"{point_name_a}_{point_name_b}_distance"] = get_point_point_distance(
        df[f"{point_name_a}_x"],
        df[f"{point_name_a}_y"],
        df[f"{point_name_a}_z"],
        df[f"{point_name_b}_x"],
        df[f"{point_name_b}_y"],
        df[f"{point_name_b}_z"],
    )
    df[f"{point_name_a}_{point_name_b}_distance_smooth"] = signal.savgol_filter(
        df[f"{point_name_a}_{point_name_b}_distance"],
        window_length=11,
        polyorder=3,
        mode="nearest",
    )
    ax_floor_dist = df.plot(
        kind="line",
        x="Time",
        y=f"{point_name_a}_{point_name_b}_distance_smooth",
        label=f"Smoothed {point_name_a}-{point_name_b} distance [unit]",
    )
    df.plot(
        kind="line",
        x="Time",
        y=f"{point_name_a}_{point_name_b}_distance",
        label=f"{point_name_a}-{point_name_b} distance [unit]",
        title=f"{point_name_a}-{point_name_b} distance over time while performing Ollie",
        ax=ax_floor_dist,
    )
