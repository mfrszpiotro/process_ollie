from ..ollie import Ollie
from . import config as cfg
import pandas as pd
import pytest

# todo - currently not working due to imports
# ImportError: attempted relative import with no known parent package


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
