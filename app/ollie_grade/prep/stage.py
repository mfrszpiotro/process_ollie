from app.ollie_grade.utils import Stage
from app.ollie_grade.border_events import Empty, LiftOff
import pandas as pd


class Preparing(Stage):
    """
    todo
    """

    def __init__(self, start: Empty, finish: LiftOff, context: pd.DataFrame):
        super().__init__(start, finish, context)
