from .ollie import Ollie
from .events import *
from .stages import *
from pydantic import BaseModel

## Find the best match with the canonical recursion formula
from dtw import *
import matplotlib.pyplot as plt


class HowClose(BaseModel):
    absolute: float
    absolute_percent: float
    is_negative: bool
    context: str = "commit_time_diff - reference_time_diff"


class TimeTwoEvents(BaseModel):
    diff_name: str
    event_a_name: str
    event_b_name: str
    time_diff_commit: float
    time_diff_reference: float
    how_close: HowClose
    diff_description: str = """A time difference between two events is calculated for each Ollie performance (commit and reference). 
Then those time differences are compared to determine how close the both intervals are, 
and in which direction the next commit should be taken.
"""


class Grade:
    """Comparing class for two Ollie objects which is used to gain useful comparison results."""

    commit: Ollie
    reference: Ollie
    time_two_events_scenarios: dict[tuple]

    def __init__(self, commit: Ollie, reference: Ollie) -> None:
        self.commit = commit
        self.reference = reference
        self.time_two_events_scenarios = [
            (TopHeight, FrontLiftOff),
            (BackLiftOff, FrontLiftOff),
            (TopHeight, TopAngle),
        ]
        pass

    def __get_time_two_events_diff(  # todo as init of a TimeTwoClass?
        self, event_a_type: type, event_b_type: type
    ) -> TimeTwoEvents:
        com_event_a = self.commit.get_unique_event(event_a_type)
        com_event_b = self.commit.get_unique_event(event_b_type)
        ref_event_a = self.reference.get_unique_event(event_a_type)
        ref_event_b = self.reference.get_unique_event(event_b_type)
        com_diff = com_event_a.time - com_event_b.time
        ref_diff = ref_event_a.time - ref_event_b.time
        how_close = com_diff - ref_diff
        return TimeTwoEvents(
            diff_name=TimeTwoEvents.__name__,
            event_a_name=event_a_type.__name__,
            event_b_name=event_b_type.__name__,
            time_diff_commit=round(com_diff, 3),
            time_diff_reference=round(ref_diff, 3),
            how_close=HowClose(
                absolute=abs(round(how_close, 3)),
                absolute_percent=abs(round(100 * (how_close) / ref_diff, 3)),
                is_negative=bool(how_close < 0),
            ),
        )

    # todo get stage based on type?
    def __compare_dtw_diff(self, column_of_interest="crotch_angle_smooth"):
        query = self.commit.rise.stage_context[column_of_interest].to_numpy()
        template = self.reference.rise.stage_context[column_of_interest].to_numpy()
        alignment = dtw(query, template, keep_internals=True)

        ## Display the warping curve, i.e. the alignment curve
        # alignment.plot(type="threeway")

        ## Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
        output_dtw = dtw(
            query,
            template,
            keep_internals=True,
            step_pattern=rabinerJuangStepPattern(6, "c"),
        )

        output_dtw.plot(type="twoway")

        from ..scripts.point_floor_distance import add_and_plot as floor_plot
        from ..scripts.angle import add_and_plot as angle_plot

        angle_plot(self.commit.context)
        angle_plot(self.reference.context)

        ## See the recursion relation, as formula and diagram
        # print(rabinerJuangStepPattern(6, "c"))
        # rabinerJuangStepPattern(6, "c").plot()
        plt.show()
        pass

    def compare(self) -> list:
        results = []
        # self.__compare_dtw_diff()
        for scenario in self.time_two_events_scenarios:
            results.append(self.__get_time_two_events_diff(*scenario))
        return results
