import numpy as np
import pandas as pd
from scipy import signal


def get_point_distance_from_floor(
    colx: pd.Series,
    coly: pd.Series,
    colz: pd.Series,
    floorx: pd.Series,
    floory: pd.Series,
    floorz: pd.Series,
    floorw: pd.Series,
) -> pd.Series:
    numerator = colx * floorx + coly * floory + colz * floorz + floorw
    denominator = np.sqrt(floorx * floorx + floory * floory + floorz * floorz)

    return numerator / denominator


# RIGHT FOOT-FLOOR DISTANCE
def add_and_plot(df: pd.DataFrame):
    df["foot_floor_distance"] = get_point_distance_from_floor(
        df.FootRight_x,
        df.FootRight_y,
        df.FootRight_z,
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )
    df["foot_floor_distance_smooth"] = signal.savgol_filter(
        df["foot_floor_distance"], window_length=11, polyorder=3, mode="nearest"
    )
    ax_floor_dist = df.plot(
        kind="line",
        x="Time",
        y="foot_floor_distance_smooth",
        label="Smoothened foot-floor distance [unit]",
    )
    df.plot(
        kind="line",
        x="Time",
        y="foot_floor_distance",
        label="Foot-floor distance [unit]",
        title="Foot-floor distance over time while performing Ollie",
        ax=ax_floor_dist,
    )
