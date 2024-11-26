import logging

from abc import ABC
from abc import abstractmethod
from enum import Enum

from optiface import ui
from optiface.core import iinstance
from optiface.core import solution
from optiface.datamodel import feature


class SolverStatus(Enum):
    RESET = 0
    CONFIGURED = 1
    READ = 2
    # Can add solve status codes here.


class ISolver(ABC):
    """
    Interface for a solver that solves instances of the computational problem.
    """

    def __init__(self, problem_name: str) -> None:
        self._parameters: feature.FeatureValueDict
        self._status: SolverStatus = SolverStatus.RESET
        self._problem_name: str = problem_name

    def __str__(self) -> str:
        s: str = f"{self._status.name} {self._problem_name} solver"

        if self._parameters:
            s += f": {self._parameters}"

        return s

    def configure(self, parameters: feature.FeatureValueDict) -> None:
        self._parameters = parameters
        self._status = SolverStatus.CONFIGURED

    @abstractmethod
    def read_from_instance(self, instance: iinstance.IInstance) -> None:
        self._status = SolverStatus.READ

    @abstractmethod
    def solve(self) -> solution.Solution:
        pass

    @abstractmethod
    def reset(self) -> None:
        self._status = SolverStatus.RESET
