from app.ollie_grade.ollie import Ollie
import app.config as cfg
import pandas as pd
import os

filepath = cfg.OK_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie_ok = Ollie(df, "okay")
filepath = cfg.GOOD_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie_good = Ollie(df, "damn good")

print(repr(ollie_good), repr(ollie_ok))
