from app.ollie_grade.ollie import Ollie
import app.config as cfg
import pandas as pd
import os

filepath = cfg.OK_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie = Ollie(df)
print("Hello World!")
