from app.ollie_grade.utils import Stage
from app.ollie_grade.border_events import FrontLiftOff, TopHeight
from app.ollie_grade.rise.events import TopAngle
import pandas as pd


class Rising(Stage):
    """
    todo
    """

    top_angle: TopAngle

    def __init__(
        self, start: FrontLiftOff, finish: TopHeight, whole_context: pd.DataFrame
    ):
        super().__init__(start, finish, whole_context)
        self.start = start
        self.angle = self.find_top_angle_event()
        self.finish = finish

    def find_top_angle_event(self):
        """
        todo
        """
        pass
