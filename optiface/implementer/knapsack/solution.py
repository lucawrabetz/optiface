import os
from typing import Any

from optiface import ui
from optiface.datamodel import feature
from optiface.implementer import featureset
from optiface.core import solution


class KnapsackSolution(solution.Solution):
    """
    Class for a solution to the knapsack problem.
        - list of bools of size n
        - objective value
    """
