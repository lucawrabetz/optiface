from abc import ABC
from abc import abstractmethod
from enum import Enum

from optiface import ui
from optiface.datamodel import feature


class InstanceStatus(Enum):
    RESET = 0
    CONFIGURED = 1
    READ = 2


class IInstance(ABC):
    """
    Interface for an instance of the computational problem.
    """

    def __init__(self, problem_name: str):
        self._parameters: feature.FeatureValueDict = dict()
        self._filepath: str = ""
        self._status: InstanceStatus = InstanceStatus.RESET
        self._problem_name: str = problem_name

    def __str__(self) -> str:
        s: str = f"{self._status.name} {self._problem_name} instance"

        if self._parameters:
            s += f": {self._parameters}"

        return s

    def configure(
        self, parameters: feature.FeatureValueDict, filepath: str = ""
    ) -> None:
        # TODO (LW / PS): I think make sure set_name is first parameter and rep is last parameter (out of instance parameters). Related - enforcing required / starting parameters (starting schema), but not let anyone change it, and certain orders either.
        # TODO (LW): resolve issue #17.
        self._parameters = parameters
        for key in parameters:
            getter = lambda self, k=key: self._parameters[k]
            setattr(self.__class__, key, property(fget=getter))
        self._filepath = filepath
        if self._filepath == "":
            ui.body(f"Configured unsaved instance [opti-face]:")
        else:
            ui.body(f"Configured instance from {filepath} [opti-face]:")
        ui.body(self.__str__())
        self._status = InstanceStatus.CONFIGURED

    @property
    def filepath(self) -> str:
        return self._filepath

    @abstractmethod
    def read(self) -> None:
        self._status = InstanceStatus.READ

    @abstractmethod
    def reset(self) -> None:
        self._parameters = dict()
        self._filepath = ""
        self._status = InstanceStatus.RESET
