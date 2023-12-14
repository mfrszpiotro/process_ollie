from app.ollie_grade.ollie import Ollie
import app.ollie_grade.tests.config as cfg
import pandas as pd
import pytest


@pytest.mark.parametrize(
    "filepath, expected_result",
    [
        (cfg.GOOD_OLLIE_TEST_FILE_PATH, True),
        (cfg.OK_OLLIE_TEST_FILE_PATH, True),
        (cfg.EMPTY_OLLIE_TEST_FILE_PATH, False),
    ],
)
def test_stages_not_empty(filepath, expected_result):
    df = pd.read_csv(filepath)
    ollie = Ollie(df, "test")
    actual_result = len(ollie.context) != 0
    assert actual_result == expected_result
