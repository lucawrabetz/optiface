import os
from typing import Any

from optiface import ui
from optiface.datamodel import feature
from optiface.implementer import optiinit
from optiface.implementer import optispace
from optiface.core import iinstance


class KnapsackInstance(iinstance.IInstance):
    """
    Class for an instance of the knapsack problem (https://en.wikipedia.org/wiki/Knapsack_problem), specifically the 0-1 knapsack problem.
        - Parameters: n - number of items.
        - Data: weights (n integers), values (n integers), capacity (integer).
        - Line by line file expected:
            - line 0: capacity
            - line i > 0: weight_i value_i
    """

    def read(self) -> None:
        self._weights: list[int | None] = [None] * self.n
        self._values: list[int | None] = [None] * self.n
        self._capacity: int = -1
        ui.body(f"Reading knapsack instance from file {self._filepath} [implementer]")
        with open(self.filepath) as f:
            i = -1
            for line in f:
                line.rstrip("\n")
                if i == -1:
                    self._capacity = int(line[0])
                else:
                    vals = [int(s) for s in line.split(" ")]
                    self._weights[i] = vals[0]
                    self._values[i] = vals[0]
                i += 1
        ui.body(f"Read Knapsack Instance {self.filepath} [implementer]")

    def reset(self) -> None:
        super().reset()
        self._weights = []
        self._values = []
        self._capacity = -1
        ui.body("Knapsack instance reset [implementer]")

    def log_data(self) -> None:
        ui.subheader("Knapsack instance:")
        for i in range(self.n):
            ui.body(
                f"\titem {str(i+1)}: weight {self._weights[i]}, value {self._values[i]}"
            )
        ui.blank_line()
        ui.body(f"\tcapacity: {self._capacity}")


# TODO - this should be in optiface_init
PROBLEM_INSTANCE = KnapsackInstance


def main() -> None:
    fs: optispace.ProblemSpace = optiinit.optiface_init()
    params: feature.FeatureValueDict = {
        i.name: (i, i.default) for i in fs.instance_key.values()
    }
    kpinstance: KnapsackInstance = KnapsackInstance()
    kpinstance.configure(parameters=params)


if __name__ == "__main__":
    main()
