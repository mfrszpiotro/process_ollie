import pandas as pd
from pandas import Series
from enum import Enum


class PointsOfInterest(Enum):
    ANKLE_LEFT = "AnkleLeft"
    ANKLE_RIGHT = "AnkleRight"
    HIP_LEFT = "HipLeft"
    HIP_RIGHT = "HipRight"
    CROTCH_ANGLE = "crotch_angle"  # derived not from kinect, but from processing


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


class BackLiftOff(Event):
    """
    Ollie event which indicates launch of the back foot into the air.
    """

    def __init__(self, context: Series, is_goofy: bool):
        super().__init__(
            context, f"{BackLiftOff.get_point_of_interest(is_goofy)}_deck_distance"
        )

    @staticmethod
    def get_point_of_interest(is_goofy: bool) -> str:
        return (
            PointsOfInterest.ANKLE_LEFT.value
            if is_goofy
            else PointsOfInterest.ANKLE_RIGHT.value
        )


class FrontLiftOff(Event):
    """
    Ollie border (fundamental) event which indicates launch of the front foot into the air.
    """

    def __init__(self, context: Series, is_goofy: bool):
        super().__init__(
            context, f"{FrontLiftOff.get_point_of_interest(is_goofy)}_deck_distance"
        )

    @staticmethod
    def get_point_of_interest(is_goofy: bool) -> str:
        return (
            PointsOfInterest.ANKLE_RIGHT.value
            if is_goofy
            else PointsOfInterest.ANKLE_LEFT.value
        )


class TopAngle(Event):
    """
    todo
    """

    def __init__(self, context: Series, interest_column=PointsOfInterest.CROTCH_ANGLE):
        super().__init__(context, interest_column)


class TopHeight(Event):
    """
    Ollie border (fundamental) event which indicates the highest point reached (usually of the front hip point) during the performance.
    """

    def __init__(self, context: Series, is_goofy: bool):
        super().__init__(
            context, f"{TopHeight.get_point_of_interest(is_goofy)}_floor_distance"
        )

    @staticmethod
    def get_point_of_interest(is_goofy: bool) -> str:
        return (
            PointsOfInterest.HIP_RIGHT.value
            if is_goofy
            else PointsOfInterest.HIP_LEFT.value
        )


class Landed(Event):
    """
    Ollie border (fundamental) event which indicates the moment when (usually) front foot lands on the ground with the board.
    """

    def __init__(self, context: Series, is_goofy: bool):
        super().__init__(
            context, f"{Landed.get_point_of_interest(is_goofy)}_deck_distance"
        )

    @staticmethod
    def get_point_of_interest(is_goofy: bool) -> str:
        return (
            PointsOfInterest.ANKLE_RIGHT.value
            if is_goofy
            else PointsOfInterest.ANKLE_LEFT.value
        )
