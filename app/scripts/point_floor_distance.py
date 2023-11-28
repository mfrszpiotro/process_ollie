import numpy as np
import pandas as pd
from scipy import signal
import os


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


def save_strip_to_jump(
    df: pd.DataFrame, relative_path, subfolder, filename, jump_point_factor="HipRight"
):
    df = strip_to_jump(df, jump_point_factor)
    full_filepath = os.path.join(relative_path, subfolder, f"jump_{filename}")
    df.to_csv(full_filepath, index=False)


def strip_to_jump(df: pd.DataFrame, jump_point_factor="HipRight") -> pd.DataFrame:
    df[f"{jump_point_factor}_floor_distance"] = get_point_distance_from_floor(
        df[f"{jump_point_factor}_x"],
        df[f"{jump_point_factor}_y"],
        df[f"{jump_point_factor}_z"],
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )
    result = df.loc[df[f"{jump_point_factor}_floor_distance"].idxmax()]
    max_index = result.name
    return df[max_index - 20 : max_index + 30]


def add_and_plot(df: pd.DataFrame, point_name="FootRight"):
    df[f"{point_name}_floor_distance"] = get_point_distance_from_floor(
        df[f"{point_name}_x"],
        df[f"{point_name}_y"],
        df[f"{point_name}_z"],
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )
    df[f"{point_name}_floor_distance_smooth"] = signal.savgol_filter(
        df[f"{point_name}_floor_distance"],
        window_length=11,
        polyorder=3,
        mode="nearest",
    )
    ax_floor_dist = df.plot(
        kind="line",
        x="Time",
        y=f"{point_name}_floor_distance_smooth",
        label=f"Smoothened {point_name}-floor distance [unit]",
    )
    df.plot(
        kind="line",
        x="Time",
        y=f"{point_name}_floor_distance",
        label=f"{point_name}-floor distance [unit]",
        title=f"{point_name}-floor distance over time while performing Ollie",
        ax=ax_floor_dist,
    )
