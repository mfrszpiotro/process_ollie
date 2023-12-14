from .utils import Event
from pandas import Series


class Empty(Event):
    """
    todo
    """

    def __init__(self, context: Series):
        super().__init__(context, None)


class FrontLiftOff(Event):
    """
    Ollie event which indicates launch of the front foot into the air.
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_deck_distance")


class TopHeight(Event):
    """
    todo
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_floor_distance")


class Landed(Event):
    """
    todo
    """

    def __init__(self, context: Series, jump_point_factor):
        super().__init__(context, f"{jump_point_factor}_deck_distance")
