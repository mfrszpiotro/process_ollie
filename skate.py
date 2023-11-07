import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt

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

plt.close("all")
df = pd.read_csv('data\\setup_mid\\good\\20231106_1224\\trimmed - 20231106122417713.csv')
crotch_data = df[["Time",
                  "KneeRight_x",  "KneeRight_y",  "KneeRight_z",
                  "HipRight_x",   "HipRight_y",   "HipRight_z",
                  "KneeLeft_x",   "KneeLeft_y",   "KneeLeft_z",   
                  "HipLeft_x",    "HipLeft_y",    "HipLeft_z"]]

crotch_data["crotch_angle"] = crotch_data.apply(
    lambda row: calc_angle(row[1:4], row[4:7], row[7:10], row[10:13]), axis=1)

print(crotch_data)
crotch_data.plot(kind="line", x="Time", y="crotch_angle", label="Crotch angle [deg]", 
        title="Crotch angle over time while performing Ollie")
plt.show()