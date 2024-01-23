from ..stage import Stage
from ..event import Empty, Landed
import pandas as pd


class Landing(Stage):
    """
    todo
    """

    def __init__(self, start: Landed, finish: Empty, context: pd.DataFrame):
        super().__init__(start, finish, context)
