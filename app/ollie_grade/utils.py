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
        self.time = context.loc["Time"]
        self.interest_column = interest_column


class Stage:
    """
    todo
    """

    whole_context: pd.DataFrame
    stage_context: pd.DataFrame

    def __init__(self, start: Event, finish: Event, whole_context: pd.DataFrame):
        self.start = start
        self.finish = finish
        self.whole_context = whole_context
        self.stage_context = self.__strip_to_stage()

    def __strip_to_stage(self) -> pd.DataFrame:
        df = self.whole_context
        start_id = df.index[df.Time == self.start.time].to_list()
        finish_id = df.index[df.Time == self.finish.time].to_list()
        if len(start_id) > 1 or len(finish_id) > 1:
            raise Exception("Duplicated time instants were found.")
        return df[start_id[0] : finish_id[0]]
