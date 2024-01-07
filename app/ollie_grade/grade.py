from .ollie import Ollie
from .utils import Event
from .border_events import *


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
        return {
            self.commit.name: com_diff,
            self.reference.name: ref_diff,
            "time_diff": com_diff - ref_diff,
        }

    def compare(self) -> list[dict]:
        results = []
        example_diff = self.__compare_events_time_diff(FrontLiftOff, TopHeight)
        results.append(example_diff)
        return results
