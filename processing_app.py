from app.ollie_grade.ollie import Ollie
from app.ollie_grade.grade import Grade
import app.config as cfg
import app.ollie_grade.tests.config as test_cfg
import pandas as pd
import os

filepath = test_cfg.OK_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie_ok = Ollie(df, "okay")
filepath = test_cfg.GOOD_OLLIE_TEST_FILE_PATH
df = pd.read_csv(filepath)
ollie_good = Ollie(df, "damn good")

print(repr(ollie_good), repr(ollie_ok))
comparator = Grade(ollie_ok, ollie_good)
print(f"Comparing results: {comparator.compare()}")
