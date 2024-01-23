import pandas as pd
from pandas import Series


class Event:
    """
    todo
    """

    context: pd.Series
    time: float
    interest_column: str

    def __init__(self, context: pd.Series, interest_column: str | None):
        self.context = context
        self.time = context.loc["Time"]
        self.interest_column = interest_column


class Empty(Event):
    """
    Ollie placeholder event which should indicate the end of the context data (not implemented one).
    """

    def __init__(self, context: Series):
        super().__init__(context, None)


class FrontLiftOff(Event):
    """
    Ollie border (fundamental) event which indicates launch of the front foot into the air.
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_deck_distance")


class TopHeight(Event):
    """
    Ollie border (fundamental) event which indicates the highest point reached (usually of the front hip point) during the performance.
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_floor_distance")


class Landed(Event):
    """
    Ollie border (fundamental) event which indicates the moment when (usually) front foot lands on the ground with the board.
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_deck_distance")
