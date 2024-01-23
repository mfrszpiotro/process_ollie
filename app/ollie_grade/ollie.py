from .event import *
from .rise.events import *
from .prep.stage import Preparing
from .rise.stage import Rising
from .fall.stage import Falling
from .land.stage import Landing
from ..scripts.point_floor_distance import (
    add,
    find_max_distance,
    find_min_distance,
    strip_to_jump_by_time,
    find_time_bounds_indexes,
)
import pandas as pd


class Ollie:
    """Abstract definition of a skateboarding trick called "Ollie"."""

    name: str
    context: pd.DataFrame
    prep: Preparing
    rise: Rising
    fall: Falling
    land: Landing
    front_ankle: str
    front_hip: str

    def __init__(self, jump: pd.DataFrame, name: str):
        self.name = name
        self.context = strip_to_jump_by_time(jump)
        self.front_ankle = "AnkleRight"
        self.front_hip = "HipRight"
        self.prep, self.rise, self.fall, self.land = self.__form_stages(
            *Ollie.__find_basic_events(jump)
        )
        pass

    def __repr__(self):
        return f"""
Ollie "{self.name}" conists of four stages:
    - Preparation: {self.prep.stage_context.shape}
    - Rising: {self.rise.stage_context.shape}
    - Falling: {self.fall.stage_context.shape}
    - Landing: {self.land.stage_context.shape}
Whole ollie shape: {self.context.shape}
"""

    def __search_lift_off(self, top: TopHeight) -> FrontLiftOff:
        """Search front foot lift off based on TopHeight event.

        Args:
            top (TopHeight): Top height record of the Ollie.

        Returns:
            FrontLiftOff: Event which indicates launch of the front foot into the air.
        """
        point_of_interest = self.front_ankle
        lift_off_series = Ollie.__search_min_floor_series(
            self.context, 0.4, 0, top.time, point_of_interest
        )
        return FrontLiftOff(lift_off_series, point_of_interest)

    def __search_landed(self, top: TopHeight) -> Landed:
        """Search landing event based on TopHeight event.

        Args:
            top (TopHeight): Top height record of the Ollie.

        Returns:
            Landed: Event which indicates landing on the ground after the jump.
        """
        point_of_interest = self.front_ankle
        landed_series = Ollie.__search_min_floor_series(
            self.context, 0, 0.5, top.time, point_of_interest
        )
        return Landed(landed_series, point_of_interest)

    def __form_stages(
        self, start: Empty, top: TopHeight, finish: Empty
    ) -> (Preparing, Rising, Falling, Landing):
        lift_off = self.__search_lift_off(top)
        landed = self.__search_landed(top)
        prep = Preparing(start, lift_off, self.context)
        rise = Rising(lift_off, top, self.context)
        fall = Falling(top, landed, self.context)
        land = Landing(landed, finish, self.context)
        return prep, rise, fall, land

    @staticmethod
    def __find_basic_events(
        jump: pd.DataFrame,
    ) -> (Empty, TopHeight, Empty):
        start_series = jump.iloc[0]
        start = Empty(start_series)
        top_height_factor = "HipRight"
        top_height_series = find_max_distance(jump, top_height_factor)
        top_height = TopHeight(top_height_series, top_height_factor)
        end_series = jump.iloc[-1]
        end = Empty(end_series)
        return (start, top_height, end)

    @staticmethod
    def __search_min_floor_series(
        context: pd.DataFrame,
        time_from: float,
        time_to: float,
        reference_time: float,
        search_column: str,
    ) -> pd.Series:
        """A method to extract a minimal point-floor distance from the specified search interval.

        Args:
            context (pd.DataFrame): _description_
            time_from (float): Time distance before the reference time.
            time_to (float): Time distance after the reference time.
            reference_time (float): Time instant from which time_from difference and time_to difference apply - altogether it creates a search interval.
            search_column (str): A point to get the minimal distance from the floor

        Returns:
            pd.Series: A point with a minimal distance to the floor.
        """
        search_start, search_start_finish = find_time_bounds_indexes(
            context, time_from, time_to, ref_time=reference_time
        )
        search_context = context[search_start:search_start_finish]
        add(search_context, search_column)
        return find_min_distance(search_context, search_column)

    def get_unique_event(self, event_type: type) -> Event:
        found_event = None
        if event_type == FrontLiftOff:
            found_event = self.rise.start
        elif event_type == TopHeight:
            found_event = self.rise.finish
        elif event_type == Landed:
            found_event = self.fall.finish
        elif event_type == BackLiftOff:
            found_event = self.rise.back_lift_off
        elif event_type == TopAngle:
            found_event = self.rise.top_angle
        else:
            raise NotImplementedError(
                "One of the events were not found or initialized."
            )
        return found_event

    # todo
    # def compare(self, to_compare) -> dict:
    #     if isinstance(to_compare, Ollie):
    #         comparator = Grade(self, to_compare)
    #         return comparator.compare()
    #     raise TypeError
