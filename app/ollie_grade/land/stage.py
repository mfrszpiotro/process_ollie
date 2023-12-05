from app.ollie_grade.utils import Stage
from app.ollie_grade.border_events import Landed, Empty
import pandas as pd


class Landing(Stage):
    """
    todo
    """

    def __init__(self, start: Landed, finish: Empty, context: pd.DataFrame):
        super().__init__(start, finish, context)
