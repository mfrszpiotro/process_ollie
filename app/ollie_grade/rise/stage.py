from ..utils import Stage
from ..border_events import FrontLiftOff, TopHeight
from ..rise.events import TopAngle, BackLiftOff
import pandas as pd


class Rising(Stage):
    """
    todo
    """

    back_lift_off: BackLiftOff
    top_angle: TopAngle

    def __init__(
        self, start: FrontLiftOff, finish: TopHeight, whole_context: pd.DataFrame
    ):
        super().__init__(start, finish, whole_context)
        self.back_lift_off = self.__find_back_lift_off_event()
        self.top_angle = self.__find_top_angle_event()

    def __find_back_lift_off_event(self):
        """
        todo
        """
        pass

    def __find_top_angle_event(self):
        """
        todo
        """
        pass
