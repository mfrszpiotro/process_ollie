import pandas as pd


class Event:
    """
    todo
    """

    context: pd.Series
    time: float
    interest_column: str

    def __init__(self, context: pd.Series, interest_column: str):
        self.context = context
        self.time = context.iloc[0]
        self.interest_column = interest_column


class Stage:
    """
    todo
    """

    context: pd.DataFrame

    def __init__(self, start, finish, context: pd.DataFrame):
        self.context = context
        self.start = start
        self.finish = finish
