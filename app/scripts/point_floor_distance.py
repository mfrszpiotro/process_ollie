import numpy as np
import pandas as pd
from scipy import signal
import os
from .bounds_by_time import find_time_bounds_indexes

pd.options.mode.chained_assignment = None  # default='warn'


def _get_point_distance_from_floor(
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


def _add(df: pd.DataFrame, point_name: str):
    df[f"{point_name}_floor_distance"] = _get_point_distance_from_floor(
        df[f"{point_name}_x"],
        df[f"{point_name}_y"],
        df[f"{point_name}_z"],
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )


def add_and_plot(df: pd.DataFrame, point_name: str):
    _add(df, point_name)
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
        label=f"Smoothed {point_name}-floor distance [unit]",
    )
    df.plot(
        kind="line",
        x="Time",
        y=f"{point_name}_floor_distance",
        label=f"{point_name}-floor distance [unit]",
        title=f"{point_name}-floor distance over time while performing Ollie",
        ax=ax_floor_dist,
    )


def strip_to_jump_by_frames(
    df: pd.DataFrame,
    jump_point_factor="HipRight",
    left_dist=15,
    right_dist=30,
) -> pd.DataFrame:
    df[f"{jump_point_factor}_floor_distance"] = _get_point_distance_from_floor(
        df[f"{jump_point_factor}_x"],
        df[f"{jump_point_factor}_y"],
        df[f"{jump_point_factor}_z"],
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )
    result = find_max_distance(df, jump_point_factor)
    max_index = result.name
    return df[max_index - left_dist : max_index + right_dist]


def strip_to_jump_by_time(
    df: pd.DataFrame, jump_point_factor="HipRight", left_dist=0.5, right_dist=1.0
) -> pd.DataFrame:
    df[f"{jump_point_factor}_floor_distance"] = _get_point_distance_from_floor(
        df[f"{jump_point_factor}_x"],
        df[f"{jump_point_factor}_y"],
        df[f"{jump_point_factor}_z"],
        df.Floor_x,
        df.Floor_y,
        df.Floor_z,
        df.Floor_w,
    )
    result = find_max_distance(df, jump_point_factor)
    left_bound, right_bound = find_time_bounds_indexes(
        df, left_dist, right_dist, result["Time"]
    )
    return df[left_bound:right_bound]


def save_strip_to_jump(
    df: pd.DataFrame,
    relative_path: str,
    subfolder: str,
    filename: str,
    jump_point_factor="HipRight",
    byTime=True,
):
    if byTime:
        df = strip_to_jump_by_time(df, jump_point_factor)
    else:
        df = strip_to_jump_by_frames(df, jump_point_factor)
    full_filepath = os.path.join(relative_path, subfolder, f"jump_{filename}")
    df.to_csv(full_filepath, index=False)


def find_max_distance(
    df: pd.DataFrame,
    jump_point_factor: str,
) -> pd.Series:
    max_index = df[f"{jump_point_factor}_floor_distance"].idxmax()
    max_series = df.loc[max_index]
    return max_series


def find_min_distance(
    df: pd.DataFrame,
    jump_point_factor: str,
) -> pd.Series:
    min_index = df[f"{jump_point_factor}_floor_distance"].idxmin()
    min_series = df.loc[min_index]
    return min_series


def search_min_floor_point(
    context: pd.DataFrame,
    time_from: float,
    time_to: float,
    reference_time: float,
    search_column: str,
) -> pd.Series:
    """A method to extract a minimal point-floor distance from the specified search interval.

    Args:
        context (pd.DataFrame): _description_
        time_from (float): Time distance before the reference time.
        time_to (float): Time distance after the reference time.
        reference_time (float): Time instant from which time_from difference and time_to difference apply - altogether it creates a search interval.
        search_column (str): A point to get the minimal distance from the floor

    Returns:
        pd.Series: A point with a minimal distance to the floor.
    """
    search_start, search_start_finish = find_time_bounds_indexes(
        context, time_from, time_to, ref_time=reference_time
    )
    search_context = context[search_start:search_start_finish]
    _add(search_context, search_column)
    return find_min_distance(search_context, search_column)
