import os
from typing import Any

from optiface import ui
from optiface.core import isolver
from optiface.core import solution
from optiface.datamodel import feature
from optiface.implementer import optispace


from optiface.implementer.knapsack.instance import (
    KnapsackInstance,
)  # what to import from instance


class RatioKPSolver(isolver.ISolver):
    def configure_from_instance(self, instance: KnapsackInstance) -> None:
        pass

    def solve(self) -> solution.Solution:
        pass

    def reset(self) -> None:
        pass
