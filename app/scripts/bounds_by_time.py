from bisect import bisect_left, bisect_right
import pandas as pd


def find_time_bounds_indexes(
    df: pd.DataFrame, left_seconds: float, right_seconds: float, ref_time: float
) -> (int, int):
    column_name = "Time"
    left_bound = _get_closests(df, column_name, ref_time - left_seconds)
    right_bound = _get_closests(df, column_name, ref_time + right_seconds)
    if isinstance(left_bound, tuple):
        left_bound = left_bound[0]
    if isinstance(right_bound, tuple):
        right_bound = right_bound[1]
    return left_bound, right_bound


def _get_closests(df: pd.DataFrame, column: str, search_value: float) -> tuple | int:
    lower_idx = bisect_left(df[column].values, search_value)
    higher_idx = bisect_right(df[column].values, search_value)
    if higher_idx == lower_idx:  # val is not in the list
        return lower_idx - 1, lower_idx
    else:  # val is in the list
        return lower_idx
