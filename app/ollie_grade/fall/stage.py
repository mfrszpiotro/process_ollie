from ..utils import Stage
from ..border_events import TopHeight, Landed
import pandas as pd


class Falling(Stage):
    """
    todo
    """

    def __init__(self, start: TopHeight, finish: Landed, context: pd.DataFrame):
        super().__init__(start, finish, context)
