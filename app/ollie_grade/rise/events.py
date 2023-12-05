from app.ollie_grade.utils import Event
from pandas import Series


class TopAngle(Event):
    """
    todo
    """

    def __init__(self, context: Series, interest_column="crotch_angle"):
        super().__init__(context, interest_column)
