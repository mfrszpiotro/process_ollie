from scripts import angle, point_floor_distance, point_speed
from config import DATA_DIR
import pandas as pd
import matplotlib.pyplot as plt
import os

data_directory = DATA_DIR
subfolders = []
for entry in os.scandir(data_directory):
    if not entry.is_file():
        subfolders.append(entry.name)

if subfolders:
    for index, folder in enumerate(subfolders):
        print(f"press {index} - {folder}")
    resp = int(input("Please select a subfolder to operate on: "))
    if resp in range(len(subfolders)):
        data_directory += f"\\{subfolders[resp]}"
    else:
        raise ValueError("Invalid folder index.")

for entry in os.scandir(data_directory):
    if not entry.is_file():
        continue

    plt.close("all")
    df = pd.read_csv(
        data_directory + f"\\{entry.name}",
        usecols=[
            "Time",
            "KneeRight_x",
            "KneeRight_y",
            "KneeRight_z",
            "HipRight_x",
            "HipRight_y",
            "HipRight_z",
            "KneeLeft_x",
            "KneeLeft_y",
            "KneeLeft_z",
            "HipLeft_x",
            "HipLeft_y",
            "HipLeft_z",
            "FootRight_x",
            "FootRight_y",
            "FootRight_z",
            "Floor_x",
            "Floor_y",
            "Floor_z",
            "Floor_w",
        ],
    )

    # angle.add_and_plot(df)
    # point_floor_distance.add_and_plot(df, "HipRight")
    # point_speed.add_and_plot(df)
    df = point_floor_distance.strip_to_jump(df)
    print(df)

    plt.show(block=False)
    response = input("Proceed with next file? (Y/n): ")
    if response in ("Y", "y", ""):
        continue
    if response in ("N", "n"):
        break
    else:
        raise ValueError(
            "Invalid response (write 'Y', 'y' or press Enter to proceed with files.)"
        )


print("No more files to proceed with!")
