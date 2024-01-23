from app.scripts import angle, point_floor_distance, point_speed, point_point_distance
from app.config import *
import pandas as pd
import matplotlib.pyplot as plt
import os

data_directory = INTERIM_TIME_DATA_DIR
subfolders = []
for entry in os.scandir(data_directory):
    if not entry.is_file():
        subfolders.append(entry.name)

selected_subfolder = None
if subfolders:
    for index, folder in enumerate(subfolders):
        print(f"press {index} - {folder}")
    resp = int(input("Please select a subfolder to operate on: "))
    if resp in range(len(subfolders)):
        selected_subfolder = subfolders[resp]
        data_directory += f"\\{subfolders[resp]}"
    else:
        raise ValueError("Invalid folder index.")

for entry in os.scandir(data_directory):
    if not entry.is_file():
        continue

    plt.close("all")
    filepath = os.path.join(data_directory, entry.name)
    df = pd.read_csv(
        filepath,
        usecols=USED_COLUMNS,
    )
    print(f"Loaded file: {filepath}")

    angle.add_and_plot(df)
    # point_floor_distance.add_and_plot(df, "HipRight")
    # point_floor_distance.save_strip_to_jump(df, INTERIM_TIME_DATA_DIR, selected_subfolder, entry.name)
    # point_speed.add_and_plot(df)
    # point_point_distance.add_and_plot(df)

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
