from enum import Enum

from optiface import ui
from optiface.datamodel import feature


class SolutionStatus(Enum):
    RESET = 0
    CONFIGURED = 1


class Solution:
    """
    Interface for a solution to an instance of computational problem.
    """

    def __init__(self, problem_name: str) -> None:
        self._outputs: feature.FeatureValueDict
        self._status: SolutionStatus = SolutionStatus.RESET
        self._problem_name: str = problem_name

    def __str__(self) -> str:
        s: str = f"{self._status.name} {self._problem_name} solution"
        if self._outputs:
            s += f": {self._outputs.__str__()}"

        return s

    def configure(self, outputs: feature.FeatureValueDict) -> None:
        self._outputs = outputs
        self._status = SolutionStatus.CONFIGURED

    def reset(self) -> None:
        self._outputs.clear()
        self._status = SolutionStatus.RESET
