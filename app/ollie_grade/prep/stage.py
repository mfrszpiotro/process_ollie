from ..utils import Stage
from ..border_events import Empty, FrontLiftOff
import pandas as pd


class Preparing(Stage):
    """
    todo
    """

    def __init__(self, start: Empty, finish: FrontLiftOff, whole_context: pd.DataFrame):
        super().__init__(start, finish, whole_context)
