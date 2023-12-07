from app.ollie_grade.ollie import Ollie
import app.config as cfg
import pandas as pd
import os

filepath = cfg.GOOD_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie = Ollie(df)
border_events = Ollie.find_border_events(df)
print("Hello World!")
