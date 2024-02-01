from .ollie import Ollie
from .events import *
from .stages import *
from pydantic import BaseModel
from dtw import DTW, dtw, rabinerJuangStepPattern
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


class DynamicTimeWarp(BaseModel):
    diff_name: str
    stage: str
    column_name: str
    commit_length: int
    reference_length: int
    total_distance: float
    normalized_distance: float
    html_plot: str | None = None
    diff_description: str = """Dynamic Time Warp applied for two time series from given column within a given stage.
The html_plot gives a visual comparison representation between series."""


class Grade:
    """Comparing class for two Ollie objects which is used to gain useful comparison results."""

    commit: Ollie
    reference: Ollie
    time_two_events_scenarios: list[tuple]
    dynamic_time_warp_scenarios: list[tuple]

    def __init__(self, commit: Ollie, reference: Ollie) -> None:
        self.commit = commit
        self.reference = reference
        self.time_two_events_scenarios = [
            (TopHeight, FrontLiftOff),
            (BackLiftOff, FrontLiftOff),
            (TopHeight, TopAngle),
        ]
        self.dynamic_time_warp_scenarios = [
            (Rising, "crotch_angle_smooth"),
            (Falling, "crotch_angle_smooth"),
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

    def __get_dynamic_time_warp_diff(self, stage_type: type, column_of_interest: str):
        # Get the data from the stage and the column
        stage_commit = self.commit.get_unique_stage(stage_type)
        stage_reference = self.reference.get_unique_stage(stage_type)
        query = stage_commit.stage_context[column_of_interest].to_numpy()
        template = stage_reference.stage_context[column_of_interest].to_numpy()

        ## Display the warping curve, i.e. the alignment curve
        alignment = dtw(query, template, keep_internals=True)
        alignment.plot(type="threeway")

        ## Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
        output_dtw = dtw(
            query,
            template,
            keep_internals=True,
            step_pattern=rabinerJuangStepPattern(6, "c"),
        )

        output_dtw.plot(type="twoway")

        ## See the recursion relation, as formula and diagram
        # print(rabinerJuangStepPattern(6, "c"))
        # rabinerJuangStepPattern(6, "c").plot()

        plt.show()

        return DynamicTimeWarp(
            diff_name=DynamicTimeWarp.__name__,
            stage=stage_type.__name__,
            column_name=column_of_interest,
            commit_length=output_dtw.M,
            reference_length=output_dtw.N,
            total_distance=output_dtw.distance,
            normalized_distance=output_dtw.normalizedDistance,
            # html_plot with mlpd3
        )

    def compare(self) -> list:
        results = []
        for scenario in self.time_two_events_scenarios:
            results.append(self.__get_time_two_events_diff(*scenario))
        for scenario in self.dynamic_time_warp_scenarios:
            results.append(self.__get_dynamic_time_warp_diff(*scenario))
        return results
