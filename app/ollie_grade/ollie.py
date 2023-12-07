from app.ollie_grade.border_events import *
from app.ollie_grade.prep.stage import Preparing
from app.ollie_grade.rise.stage import Rising
from app.ollie_grade.fall.stage import Falling
from app.ollie_grade.land.stage import Landing
from app.scripts.point_floor_distance import find_max_distance
import pandas as pd


class Ollie:
    """
    todo
    """

    context: pd.DataFrame
    prep: Preparing
    rise: Rising
    fall: Falling
    land: Landing

    def __init__(self, jump: pd.DataFrame):
        self.context = jump
        # self.prep, self.rise, self.fall, self.land = self.split_jump(
        #     self.find_border_events(jump)
        # )
        pass

    def split_jump(self, stages: tuple) -> (Preparing, Rising, Falling, Landing):
        pass

    @staticmethod
    def find_border_events(
        jump: pd.DataFrame,
    ) -> (Empty, LiftOff, TopHeight, Landed, Empty):
        top_height_factor = "HipRight"
        top_height_series = find_max_distance(jump, top_height_factor)
        top_height = TopHeight(top_height_series, top_height_factor)
        pass
