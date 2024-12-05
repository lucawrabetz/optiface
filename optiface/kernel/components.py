import logging

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from optiface import ui
from optiface.datamodel import feature


class ComponentStatus(Enum):
    RESET = 0
    CONFIGURED = 1
    READ = 2
    EXECUTED = 3


class SolutionStatus(Enum):
    EMPTY = 0
    INFEASIBLE = 1
    FEASIBLE = 2
    OPTIMAL = 3


@dataclass
class Solution:
    outputs: feature.FeatureValueDict = dict()
    status: SolutionStatus = SolutionStatus.EMPTY
    problem_name: str = ""  # will there be a default problem? problem 1 in the project?

    def __str__(self) -> str:
        s: str = f"[{self.status.name}] {self.problem_name} solution"
        if self.outputs:
            s += f": {self.outputs.__str__()}"

        return s

    def set_solution(
        self, outputs: feature.FeatureValueDict, status: SolutionStatus
    ) -> None:
        self.outputs = outputs
        self.status = status

    def reset(self) -> None:
        self.outputs.clear()
        self.status = SolutionStatus.EMPTY


class IComponent(ABC):
    """
    Interface for reusable components that follow an init -> configure -> read -> execute -> reset cycle.
    """

    def __init__(self) -> None:
        """
        Initialize the component. This method is called once when the object is created.
        """
        self._status: ComponentStatus = ComponentStatus.RESET

    @property
    def status(self) -> ComponentStatus:
        return self._status

    def configure(self, config: Any) -> str:
        res: str = self.configure_child(config)
        self._status = ComponentStatus.CONFIGURED
        return res

    def read(self) -> str:
        res: str = self.read_child()
        self._status = ComponentStatus.READ
        return res

    def execute(self) -> str:
        res: str = self.execute_child()
        self._status = ComponentStatus.EXECUTED
        return res

    def reset(self) -> str:
        res: str = self.reset_child()
        self._status = ComponentStatus.RESET
        return res

    @abstractmethod
    def configure_child(self, config: Any) -> str:
        pass

    @abstractmethod
    def read_child(self) -> str:
        pass

    @abstractmethod
    def execute_child(self) -> str:
        pass

    @abstractmethod
    def reset_child(self) -> str:
        pass


class Instance(IComponent):
    def __init__(self, problem_name: str):
        super().__init__()
        self._parameters: feature.FeatureValueDict = dict()
        self._filepath: str = ""
        self._problem_name: str = problem_name

    def __str__(self) -> str:
        s: str = f"{self._status.name} {self._problem_name} instance"

        if self._filepath:
            s += f" saved at {self._filepath}"

        if self._parameters:
            s += f": {self._parameters}"

        return s

    @property
    def filepath(self) -> str:
        return self._filepath

    def configure_child(
        self, config: feature.FeatureValueDict, filepath: str = ""
    ) -> str:
        # TODO (LW): resolve issue #17.
        #    - should be able to configure with just a problem name + yaml
        #    - actually not sure if parameter reading aligns with "configuration" or "init" for Instance
        self._parameters = config
        for key in self._parameters:
            getter = lambda self, k=key: self._parameters[k]
            setattr(self.__class__, key, property(fget=getter))
        self._filepath = filepath
        ui.body("configured:", special=True)
        return f"configured: {self}"

    def read_child(self) -> str:
        return ""

    def execute_child(self) -> str:
        return ""

    def reset_child(self) -> str:
        self._filepath = ""
        return self._filepath


# class Solver(IComponent):
#     def __init__(self, problem_name: str):
#         super().__init__()
#         self._parameters: feature.FeatureValueDict = dict()
#         self._problem_name: str = problem_name
#
#     def __str__(self) -> str:
#         s: str = f"{self._status.name} {self._problem_name} solver"
#
#         if self._parameters:
#             s += f": {self._parameters}"
#
#         return s
#
#     def configure(self, parameters: feature.FeatureValueDict) -> None:
#         self._parameters = parameters
#         self._status = SolverStatus.CONFIGURED
#
#     def read_child(self, instance: Instance) -> str:
#         return ""
#
#     def execute_child(self) -> str:
#         return ""
#
#     def reset_child(self) -> str:
#         self._filepath = ""
#         return self._filepath


def main():
    # start from the experiment service side
    pass


if __name__ == "__main__":
    main()
