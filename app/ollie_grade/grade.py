from .ollie import Ollie
from .events import *
from .stages import *

## Find the best match with the canonical recursion formula
from dtw import *
import numpy as np
import matplotlib.pyplot as plt


class Grade:
    """Comparing class for two Ollie objects which is used to gain useful comparison results."""

    commit: Ollie
    reference: Ollie
    comparing_scenarios: list

    def __init__(self, commit: Ollie, reference: Ollie) -> None:
        self.commit = commit
        self.reference = reference
        self.comparing_scenarios = []
        pass

    def __compare_events_time_diff(
        self, event_a_type: type, event_b_type: type
    ) -> dict:
        com_event_a = self.commit.get_unique_event(event_a_type)
        com_event_b = self.commit.get_unique_event(event_b_type)
        ref_event_a = self.reference.get_unique_event(event_a_type)
        ref_event_b = self.reference.get_unique_event(event_b_type)
        com_diff = com_event_a.time - com_event_b.time
        ref_diff = ref_event_a.time - ref_event_b.time
        how_close = com_diff - ref_diff
        return {
            "scenario_name": f"{event_a_type.__name__}&{event_b_type.__name__}",
            self.commit.name: round(com_diff, 3),
            self.reference.name: round(ref_diff, 3),
            "how_close": abs(round(how_close, 3)),
            "how_close_%": abs(round(100 * (how_close) / ref_diff, 3)),
        }

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

    def compare(self) -> list[dict]:
        results = []
        results.append(self.__compare_events_time_diff(TopHeight, FrontLiftOff))
        results.append(self.__compare_events_time_diff(BackLiftOff, FrontLiftOff))
        results.append(self.__compare_events_time_diff(TopHeight, TopAngle))
        self.__compare_dtw_diff()
        return results
