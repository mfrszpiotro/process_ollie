import pandas as pd
from .events import *
from ..scripts.point_floor_distance import search_min_floor_point
from ..scripts.angle import search_max_angle_point


class Stage:
    """
    todo
    """

    start: Event
    finish: Event
    whole_context: pd.DataFrame
    stage_context: pd.DataFrame

    def __init__(self, whole_context: pd.DataFrame, start: Event, finish: Event):
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


class Preparing(Stage):
    """
    todo
    """

    def __init__(
        self,
        whole_context: pd.DataFrame,
        start: Empty,
        jump_top_height: TopHeight,
        is_goofy: bool,
    ):
        found_finish = Preparing.__search_lift_off(
            whole_context, jump_top_height, is_goofy
        )
        super().__init__(whole_context, start, found_finish)

    @staticmethod
    def __search_lift_off(
        whole_context: pd.DataFrame, top: TopHeight, is_goofy: bool
    ) -> FrontLiftOff:
        """Search front foot lift off based on TopHeight event temporal position.

        Args:
            whole_context (pd.DataFrame): The Ollie jump performance recording.
            top (TopHeight): Top height record of the Ollie.
            is_goofy (bool): Stance of the skater (goofy = right foot in front of the riding direction).

        Returns:
            FrontLiftOff: Event which indicates launch of the front foot into the air.
        """
        point_of_interest = FrontLiftOff.get_point_of_interest(is_goofy)
        lift_off_point = search_min_floor_point(
            whole_context, 0.4, 0, top.time, point_of_interest
        )
        return FrontLiftOff(lift_off_point, is_goofy)


class Rising(Stage):
    """
    todo
    """

    back_lift_off: BackLiftOff
    top_angle: TopAngle

    def __init__(
        self,
        whole_context: pd.DataFrame,
        start: FrontLiftOff,
        jump_top_height: TopHeight,
        is_goofy: bool,
    ):
        super().__init__(whole_context, start, jump_top_height)
        self.back_lift_off = Rising.__search_lift_off(
            whole_context, jump_top_height, is_goofy
        )
        self.top_angle = Rising.__search_top_angle(whole_context, jump_top_height)

    @staticmethod
    def __search_lift_off(
        whole_context: pd.DataFrame, top: TopHeight, is_goofy: bool
    ) -> BackLiftOff:
        """Search back foot lift off based on TopHeight event temporal position.

        Args:
            whole_context (pd.DataFrame): The Ollie jump performance recording.
            top (TopHeight): Top height record of the Ollie.
            is_goofy (bool): Stance of the skater (goofy = right foot in front of the riding direction).

        Returns:
            BackLiftOff: Event which indicates launch of the back foot into the air.
        """
        point_of_interest = BackLiftOff.get_point_of_interest(is_goofy)
        lift_off_point = search_min_floor_point(
            whole_context, 0.4, 0, top.time, point_of_interest
        )
        return BackLiftOff(lift_off_point, is_goofy)

    @staticmethod
    def __search_top_angle(whole_context: pd.DataFrame, top: TopHeight) -> TopAngle:
        """Search the largest skater's crotch stretch (angle between legs) based on TopHeight event temporal position.
        It can be considered as a point where our skater has slided his foot to level-up the skateboard when performing the Ollie.

        Args:
            whole_context (pd.DataFrame): The Ollie jump performance recording.
            top (TopHeight): Top height record of the Ollie.

        Returns:
            TopAngle: Event which indicates the moment of largest skater's crotch stretch.
        """
        point_of_interest = TopAngle
        top_angle_point = search_max_angle_point(whole_context, 0.3, 0.3, top.time)
        return TopAngle(top_angle_point)


class Falling(Stage):
    """
    todo
    """

    def __init__(
        self,
        whole_context: pd.DataFrame,
        jump_top_height: TopHeight,
        is_goofy: bool,
    ):
        found_finish = Falling.__search_landed(whole_context, jump_top_height, is_goofy)
        super().__init__(whole_context, jump_top_height, found_finish)

    @staticmethod
    def __search_landed(
        whole_context: pd.DataFrame, top: TopHeight, is_goofy: bool
    ) -> Landed:
        """Search landing event based on TopHeight event.

        Args:
            top (TopHeight): Top height record of the Ollie.

        Returns:
            Landed: Event which indicates landing on the ground after the jump.
        """
        point_of_interest = Landed.get_point_of_interest(is_goofy)
        landed_point = search_min_floor_point(
            whole_context, 0, 0.5, top.time, point_of_interest
        )
        return Landed(landed_point, is_goofy)


class Landing(Stage):
    """
    todo
    """

    def __init__(
        self, whole_context: pd.DataFrame, start: Landed, finish: Empty, is_goofy: bool
    ):
        super().__init__(whole_context, start, finish)
