import os
from typing import Any

from optiface import ui
from optiface.datamodel import feature
from optiface.implementer import featureset
from optiface.core import iinstance


class KnapsackInstance(iinstance.IInstance):
    """
    Class for an instance of the knapsack problem (https://en.wikipedia.org/wiki/Knapsack_problem), specifically the 0-1 knapsack problem.
        - Parameters: n - number of items.
        - Data: weights (n integers), values (n integers), capacity (integer).
    """

    def read(self) -> None:
        # TODO: assuming for now we always read from a csv file, we will generalize this a bit or give space for more options with this contract.
        self._weights: list[int] = []
        self._values: list[int] = []
        self._capacity: int = -1
        ui.body("Reading knapsack instance [implementer]")

    def reset(self) -> None:
        self._weights = []
        self._values = []
        self._capacity = -1
        ui.body("Knapsack instance reset [implementer]")


PROBLEM_INSTANCE = KnapsackInstance


def main() -> None:
    params: feature.FeatureValueDict = {
        i.name: (i, i.default) for i in featureset.FEATURE_SPINE.instance_key
    }
    kpinstance: KnapsackInstance = KnapsackInstance()
    kpinstance.configure(parameters=params)


if __name__ == "__main__":
    main()
