from app.ollie_grade.border_events import *
from app.ollie_grade.prep.stage import Preparing
from app.ollie_grade.rise.stage import Rising
from app.ollie_grade.fall.stage import Falling
from app.ollie_grade.land.stage import Landing
from app.scripts.point_floor_distance import (
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
    front_foot: str
    front_hip: str

    def __init__(self, jump: pd.DataFrame, name: str):
        self.name = name
        self.context = strip_to_jump_by_time(jump)
        self.front_foot = "FootRight"
        self.front_hip = "HipRight"
        self.prep, self.rise, self.fall, self.land = self.__form_stages(
            *Ollie.__find_border_events(jump)
        )

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
        point_of_interest = self.front_foot
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
        point_of_interest = self.front_foot
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
    def __find_border_events(
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
    ):
        search_start, search_start_finish = find_time_bounds_indexes(
            context, time_from, time_to, ref_time=reference_time
        )
        search_context = context[search_start:search_start_finish]
        add(search_context, search_column)
        return find_min_distance(search_context, search_column)
