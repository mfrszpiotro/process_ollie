from .ollie import Ollie
from .event import *


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
            self.commit.name: round(com_diff, 3),
            self.reference.name: round(ref_diff, 3),
            "how_close": abs(round(how_close, 3)),
            "how_close_%": abs(round(100 * (how_close) / ref_diff, 3)),
        }

    def compare(self) -> list[dict]:
        results = []
        example_diff = self.__compare_events_time_diff(FrontLiftOff, TopHeight)
        results.append(example_diff)
        return results
