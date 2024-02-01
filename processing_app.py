from app.ollie_grade.ollie import Ollie
from app.ollie_grade.grade import Grade
import app.ollie_grade.tests.config as test_cfg
import pandas as pd
import json
from devtools import pprint

df = pd.read_csv(test_cfg.OK_OLLIE_TEST_FILE_PATH)
ollie_almost = Ollie(df, "almost-good", is_goofy=True)
df = pd.read_csv(test_cfg.GOOD_OLLIE_TEST_FILE_PATH)
ollie_good = Ollie(df, "good", is_goofy=True)

print(repr(ollie_good), repr(ollie_almost))
comparator = Grade(ollie_almost, ollie_good)
print(f"Comparing results:")
pprint(comparator.compare())
# json.dumps(..., default=pydantic_encoder)
