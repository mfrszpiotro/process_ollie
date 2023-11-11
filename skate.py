import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy import signal

def angle_between(v1:npt.ArrayLike, v2:npt.ArrayLike) -> float:
    """Angle calculation between two vectors is performed as follows:
    
    1. Calculate dot product v1 * v2
    2. Divide it by multiplication of magnitudes of v1 and v2.
    3. Put the result in arccos function.
    
    In other words, it is a transformed dot product equation.

    Return: Angle in radians (to obtain degrees multipliy it by: 180/pi)
    """
    
    return np.arccos(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

def calc_3d_vector(ptA:npt.ArrayLike, ptB:npt.ArrayLike) -> npt.ArrayLike:
    if len(ptA) != 3 or len(ptB) != 3:
        raise ValueError("Given point(s) are not in three dimensional space.")
    return np.subtract(ptB,ptA)

def calc_angle(ptA:pd.Series, ptB:pd.Series, ptC:pd.Series, ptD:pd.Series) -> float:
    v1 = calc_3d_vector(ptA.values, ptB.values)
    v2 = calc_3d_vector(ptC.values, ptD.values)
    # import vg
    # return vg.angle(v1, v2)
    return angle_between(v1,v2)*180/np.pi

def calc_distance_column(colx:pd.Series, coly:pd.Series, colz:pd.Series):
    p1 = np.array([colx, coly, colz])
    p2 = np.array([colx.shift(1), coly.shift(1), colz.shift(1)])

    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

plt.close("all")
df = pd.read_csv('data\\setup_mid\\good\\20231106_1224\\trimmed - 20231106122417713.csv')
df = df[["Time",
                  "KneeRight_x",  "KneeRight_y",  "KneeRight_z",
                  "HipRight_x",   "HipRight_y",   "HipRight_z",
                  "KneeLeft_x",   "KneeLeft_y",   "KneeLeft_z",   
                  "HipLeft_x",    "HipLeft_y",    "HipLeft_z",
                  "FootRight_x",  "FootRight_y",  "FootRight_z"]]

df["crotch_angle"] = df.apply(
    lambda row: calc_angle(row[1:4], row[4:7], row[7:10], row[10:13]), axis=1)

df['crotch_angle_smooth'] = signal.savgol_filter(df['crotch_angle'], window_length=11, polyorder=3, mode="nearest")

df['foot_speed'] = calc_distance_column(df.FootRight_x, df.FootRight_y, df.FootRight_z)/df.Time

df['foot_speed_smooth'] = signal.savgol_filter(df['foot_speed'], window_length=6, polyorder=3, mode="nearest")

print(df)

ax_crotch = df.plot(kind="line", x="Time", y="crotch_angle_smooth", label="Smoothened crotch angle [deg]")

df.plot(kind="line", x="Time", y="crotch_angle", label="Crotch angle [deg]", 
        title="Crotch angle over time while performing Ollie", ax=ax_crotch)

ax_foot = df.plot(kind="line", x="Time", y="foot_speed_smooth", label="Smoothened foot speed [unit/s]")

df.plot(kind="line", x="Time", y="foot_speed", label="Foot speed [unit/s]", 
        title="Foot speed over time while performing Ollie", ax=ax_foot)

plt.show()
