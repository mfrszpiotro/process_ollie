import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy import signal


def angle_between(v1: npt.ArrayLike, v2: npt.ArrayLike) -> float:
    """Angle calculation between two vectors is performed as follows:
    1. Calculate dot product v1 * v2
    2. Divide it by multiplication of magnitudes of v1 and v2.
    3. Put the result in arccos function.
    In other words, it is a transformed dot product equation.

    Args:
        v1 (npt.ArrayLike): One side of an angle (vector).
        v2 (npt.ArrayLike): Second side of an angle (vector).

    Returns:
        Angle in radians (to obtain degrees multipliy it by: 180/pi)
    """

    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def get_3d_vector(ptA: npt.ArrayLike, ptB: npt.ArrayLike) -> npt.ArrayLike:
    """Three-dimensional vector calculation from two 3D points

    Args:
        ptA (npt.ArrayLike): Vector starting point.
        ptB (npt.ArrayLike): Vector ending point.

    Raises:
        ValueError: It is required to provide vector in

    Returns:
        npt.ArrayLike: 3D vector as a straight line in space.
    """

    if len(ptA) != 3 or len(ptB) != 3:
        raise ValueError("Given point(s) are not in three dimensional space.")
    return np.subtract(ptB, ptA)


def get_angle(ptA: pd.Series, ptB: pd.Series, ptC: pd.Series, ptD: pd.Series) -> float:
    """Calculates an angle between two vectors denoted by two sets of XYZ points.

    Args:
        ptA (pd.Series): _description_
        ptB (pd.Series): _description_
        ptC (pd.Series): _description_
        ptD (pd.Series): _description_

    Returns:
        float: _description_
    """
    v1 = get_3d_vector(ptA.values, ptB.values)
    v2 = get_3d_vector(ptC.values, ptD.values)

    return angle_between(v1, v2) * 180 / np.pi


def add_and_plot(df: pd.DataFrame):
    df["crotch_angle"] = df.apply(
        lambda row: get_angle(row[1:4], row[4:7], row[7:10], row[10:13]), axis=1
    )
    df["crotch_angle_smooth"] = signal.savgol_filter(
        df["crotch_angle"], window_length=11, polyorder=3, mode="nearest"
    )
    ax_crotch = df.plot(
        kind="line",
        x="Time",
        y="crotch_angle_smooth",
        label="Smoothed crotch angle [deg]",
    )
    df.plot(
        kind="line",
        x="Time",
        y="crotch_angle",
        label="Crotch angle [deg]",
        title="Crotch angle over time while performing Ollie",
        ax=ax_crotch,
    )
