import os

from optiface import ui
from optiface import utils
from optiface.implementer import optispace
from optiface.core import iinstance


problem_name: str = "knapsack"

instance, solvers = utils.import_problem(problem_name)


def optiface_init() -> tuple[iinstance.IInstance, optispace.ProblemSpace]:
    ui.header("opti-face init...")
    problem_instance: iinstance.IInstance = instance.PROBLEM_INSTANCE(problem_name)
    fs = optispace.ProblemSpace(problem_name)
    return (problem_instance, fs)


def main() -> None:
    filepath: str = "instances/test/test_2_0.csv"
    fs, pi = optiface_init()
    ui.body(pi.__str__())
    ui.body(fs.__str__())


if __name__ == "__main__":
    main()
