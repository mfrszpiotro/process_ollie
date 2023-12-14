from app.ollie_grade.ollie import Ollie


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

    def compare(self) -> dict:
        return {}
