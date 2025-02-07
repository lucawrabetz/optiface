import importlib
from pathlib import Path

from typing import Any

from optiface.core.optispace import (
    Feature,
    ProblemSpace,
    OptiSpace,
    read_ps_from_yaml,
    read_optispace,
)

_TEST_PS_NAME: str = "testproblem"
_TEST_PS_NAME_2: str = "testproblem2"
# TODO (maybe): constant below is not DRY with constants in optiface/core/optispace.py
_TEST_PS_PATH: Path = Path("space") / _TEST_PS_NAME / "problemspace.yaml"


# TODO: unclear whether str is enough as solver "uuid" or if a solver id class is helpful
def init_data_feature_set_name() -> dict[str, Any]:
    return {
        "name": "set_name",
        "default": "test",
        "verbose_name": "Set Name",
        "short_name": "s_n",
    }


def set_name_string() -> str:
    return "feature: set_name, type: <class 'str'>, default: test, output names: 'Set Name', 's_n'"


def init_data_feature_n() -> dict[str, Any]:
    return {
        "name": "n",
        "default": -1,
        "verbose_name": "Number of Items",
        "short_name": "n",
    }


def init_data_feature_rep() -> dict[str, Any]:
    return {
        "name": "rep",
        "default": 0,
        "verbose_name": "Instance Rep",
        "short_name": "i_rep",
    }


def init_data_feature_solver() -> dict[str, Any]:
    return {
        "name": "solver",
        "default": "MySolver",
        "verbose_name": "Solver",
        "short_name": "sol",
    }


def init_data_feature_objective() -> dict[str, Any]:
    return {
        "name": "objective",
        "default": -1.0,
        "verbose_name": "Objective",
        "short_name": "obj",
    }


def init_data_feature_time_ms() -> dict[str, Any]:
    return {
        "name": "time_ms",
        "default": -1.0,
        "verbose_name": "Running Time (ms)",
        "short_name": "t_ms",
    }


def init_test_problem_space() -> ProblemSpace:
    return ProblemSpace(
        name=_TEST_PS_NAME,
        instance_key={
            "set_name": Feature(**init_data_feature_set_name()),
            "n": Feature(**init_data_feature_n()),
            "rep": Feature(**init_data_feature_rep()),
        },
        solver_key={"solver": Feature(**init_data_feature_solver())},
        outputs={
            "objective": Feature(**init_data_feature_objective()),
            "time_ms": Feature(**init_data_feature_time_ms()),
        },
        filepath=str(_TEST_PS_PATH),
    )


class TestSetup:
    def test_optiface_import(self):
        importlib.import_module("optiface")


class TestFeature:
    """
    Behaviors:
    - initializes a Feature as expected
    """

    def test_feature_init(self):
        set_name_raw = init_data_feature_set_name()
        set_name = Feature(**set_name_raw)
        assert set_name.name == set_name_raw["name"]
        assert set_name.default == set_name_raw["default"]
        assert set_name.verbose_name == set_name_raw["verbose_name"]
        assert set_name.short_name == set_name_raw["short_name"]
        assert str(set_name) == set_name_string()


class TestProblemSpace:
    """
    Behaviors:
    - read a problem space as expected
    """

    def test_ps_read(self):
        test_ps = init_test_problem_space()
        read_ps = read_ps_from_yaml(name=_TEST_PS_NAME)
        assert test_ps == read_ps


class TestOptiSpace:
    """
    - start with just a list of problem names
    - list will be managed by PSM
    Behaviors:
    - initialization behaviors
    """

    def test_init_optispace(self):
        optispace: OptiSpace = read_optispace()
        problems = set(optispace.problems)
        assert _TEST_PS_NAME in problems
        assert _TEST_PS_NAME_2 in problems


class TestPSM:
    """
    - write a top-level function (maybe even exported, in optiface/__init__.py to get a problem space)
    - psm only needs to have a wizard to take input, and write functionality to yaml
    - "switching" ps just means calling the top-level function to refresh or read a different one
    Behaviors:
    - switch between problem spaces as expected
    """

    def test_ps_switch(self):
        """
        TODO: active problem - is a state that is not yet tracked on optispace
        - make a global problem space object, just one
        - the active problem is the name attribute
        """
        assert False

    def test_ps_add(self):
        """
        add new problem
            - add new problem with psm wizard
            - check that problemspace.yaml file is correct
            - check that optispace is updated (1 new problem name)
        """
        assert False

    def test_ps_add_feature(self):
        """
        add new feature to problemspace
        """
        assert False
