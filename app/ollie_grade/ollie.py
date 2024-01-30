from .events import *
from .stages import *
from ..scripts.point_floor_distance import (
    find_max_distance,
    strip_to_jump_by_time,
)
from ..scripts.angle import _add as add_angle_columns
import pandas as pd


class Ollie:
    """An abstract definition of a skateboarding trick called "Ollie"."""

    name: str
    context: pd.DataFrame
    prep: Preparing
    rise: Rising
    fall: Falling
    land: Landing
    is_goofy: bool

    def __init__(self, jump: pd.DataFrame, name: str, is_goofy: bool):
        self.name = name
        self.context = strip_to_jump_by_time(jump)
        self.context = add_angle_columns(self.context)
        jump_start, jump_top_height, jump_finish = Ollie.__find_basic_events(
            jump, is_goofy
        )
        self.prep = Preparing(self.context, jump_start, jump_top_height, is_goofy)
        self.rise = Rising(self.context, self.prep.finish, jump_top_height, is_goofy)
        self.fall = Falling(self.context, jump_top_height, is_goofy)
        self.land = Landing(self.context, self.fall.finish, jump_finish, is_goofy)
        self.is_goofy = is_goofy
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

    @staticmethod
    def __find_basic_events(
        whole_jump_context: pd.DataFrame, is_goofy: bool
    ) -> (Empty, TopHeight, Empty):
        start_series = whole_jump_context.iloc[0]
        start = Empty(start_series)
        top_height = TopHeight(
            find_max_distance(
                whole_jump_context, TopHeight.get_point_of_interest(is_goofy)
            ),
            is_goofy,
        )
        end_series = whole_jump_context.iloc[-1]
        end = Empty(end_series)
        return (start, top_height, end)

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
