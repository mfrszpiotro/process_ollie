from ..stage import Event
from pandas import Series


class BackLiftOff(Event):
    """
    Ollie event which indicates launch of the back foot into the air.
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_deck_distance")


class TopAngle(Event):
    """
    todo
    """

    def __init__(self, context: Series, interest_column="crotch_angle"):
        super().__init__(context, interest_column)
