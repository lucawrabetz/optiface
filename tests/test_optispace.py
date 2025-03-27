import importlib
from pathlib import Path

from typing import Any

from optiface.core.optispace import (
    Feature,
    ProblemSpace,
    OptiSpace,
    read_pspace_from_yaml,
    read_ospace,
)

######### VERY IMPORTANT #########

# note: case insensitive conventions
# ProblemSpace, problemspace, PrOblemsPace are the same

# ProblemSpace - always refers to the ProblemSpace class
# pspace - refers to an arbitrary problem space

# OptiSpace - always refers to the OptiSpace class
# ospace - refers to this opti space

##################################

_PSPACE_YAML = "problemspace.yaml"
_EXPERIMENTS_DB = "experiments.db"

_TEST_PSPACE_NAME: str = "testproblem"
# TODO: move problemspace.yaml and experiments.db to optiface/core/optispace.py
_TEST_PSPACE_PATH: Path = Path("space") / _TEST_PSPACE_NAME / _PSPACE_YAML
_TEST_PSPACEDB_PATH: Path = Path("space") / _TEST_PSPACE_NAME / _EXPERIMENTS_DB


# TODO: unclear to me whether str is enough as solver "uuid" or if a solver id class is helpful
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
        name=_TEST_PSPACE_NAME,
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
        filepath=str(_TEST_PSPACE_PATH),
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
    - note that this is testing the ProblemSpace class
    """

    def test_pspace_read(self):
        test_pspace = init_test_problem_space()
        read_pspace = read_pspace_from_yaml(name=_TEST_PSPACE_NAME)
        assert test_pspace == read_pspace


class TestOptiSpace:
    """
    - start with just a list of problem names, managed by OSM

    Behaviors (ospace):
    - every problem name is correctly read, and filepath correctly constructed
    - every pspace:
        - (problemspace.yaml) every feature has a name (str), default (str), verbose_name (str), short_name (str)
        - (problemspace.yaml <-> experiments.db match)
    """

    def test_ospace(self):
        ospace: OptiSpace = read_ospace()
        assert _TEST_PSPACE_NAME in set(ospace.problems)

        for problem in ospace.problems:
            # ProblemSpace is a BaseModel, so pydantic checks its types (right Pete?).
            # We will still assert some types for excessive testing.

            # TODO: make sure that once you do OSM, switch current
            # ospace.current = problem
            pspace: ProblemSpace = read_pspace_from_yaml(problem)
            assert isinstance(pspace.name, str)
            assert pspace.name == problem
            assert isinstance(pspace.filepath, Path)

            for f_name, f in pspace.instance_key.items():
                assert isinstance(f_name, str)
                assert f_name == f.name
                assert f.default is not None
                assert isinstance(f.verbose_name, str)
                assert len(f.verbose_name) > 0
                assert isinstance(f.short_name, str)
                assert len(f.short_name) > 0


class TestOSM:
    """
    - OSM is a user <-> optispace API: so pspace yamls can (eventually) stay locked and safe
        - add new pspace
        - add feature to pspace *
        - remove feature from pspace *
        - switch active pspace
    - * includes dbmanager interaction (add or remove columns from databases)

    Behaviors:
    - add new pspace
    - switch pspaces
    """

    def test_ps_add(self):
        assert True

    def test_pspace_add_feature(self):
        assert True

    def test_pspace_remove_feature(self):
        assert True

    def test_pspace_switch(self):
        assert True
