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


# RIGHT FOOT SPEED
def add_and_plot(df: pd.DataFrame):
    df["foot_speed"] = get_point_speed(
        df.FootRight_x, df.FootRight_y, df.FootRight_z, df.Time
    )
    df["foot_speed_smooth"] = signal.savgol_filter(
        df["foot_speed"], window_length=6, polyorder=3, mode="nearest"
    )
    ax_foot = df.plot(
        kind="line",
        x="Time",
        y="foot_speed_smooth",
        label="Smoothened foot speed [unit/s]",
    )
    df.plot(
        kind="line",
        x="Time",
        y="foot_speed",
        label="Foot speed [unit/s]",
        title="Foot speed over time while performing Ollie",
        ax=ax_foot,
    )
