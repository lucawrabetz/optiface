import importlib
import pytest

from pathlib import Path
from typing import Any
from optiface.core.optidatetime import OptiDateTimeFactory
from optiface.core.optispace import (
    yaml_to_feature_type,
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

_SPACE = "space"
_PSPACE_YAML = "problemspace.yaml"

_DEFAULT_PSPACE_NAME: str = "defaultproblem"
# TODO: move problemspace.yaml and experiments.db to optiface/core/optispace.py
_DEFAULT_PSPACE_PATH: Path = Path(_SPACE) / _DEFAULT_PSPACE_NAME / _PSPACE_YAML

opti_dt = OptiDateTimeFactory()


def init_data_feature_run_id() -> dict[str, Any]:
    return {
        "name": "run_id",
        "default": -1,
        "verbose_name": "Run Id",
        "short_name": "run_id",
        "feature_type": "int",
    }


def init_data_feature_timestamp_added() -> dict[str, Any]:
    return {
        "name": "timestamp_added",
        "default": opti_dt.optidefault(),
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type": "datetime",
    }


def init_data_feature_added_from() -> dict[str, Any]:
    return {
        "name": "added_from",
        "default": "RUN",
        "verbose_name": "Added From",
        "short_name": "from",
        "feature_type": "str",
    }


def init_data_feature_set_name() -> dict[str, Any]:
    return {
        "name": "set_name",
        "default": "test",
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type": "str",
    }


def init_data_feature_set_name_unknown_type() -> dict[str, Any]:
    return {
        "name": "set_name",
        "default": "test",
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type": "what_is_this_type",
    }


def init_data_feature_set_name_mistyped() -> dict[str, Any]:
    return {
        "name": "set_name",
        "default": "test",
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type": "int",
    }


def init_data_feature_n() -> dict[str, Any]:
    return {
        "name": "n",
        "default": -1,
        "verbose_name": "Number of Items",
        "short_name": "n",
        "feature_type": "int",
    }


def init_data_feature_rep() -> dict[str, Any]:
    return {
        "name": "rep",
        "default": 0,
        "verbose_name": "Instance Rep",
        "short_name": "i_rep",
        "feature_type": "int",
    }


# TODO: unclear to me whether str is enough as solver "uuid" or if a solver id class is helpful
def init_data_feature_solver() -> dict[str, Any]:
    return {
        "name": "solver",
        "default": "MySolver",
        "verbose_name": "Solver",
        "short_name": "sol",
        "feature_type": "str",
    }


def init_data_feature_objective() -> dict[str, Any]:
    return {
        "name": "objective",
        "default": -1.0,
        "verbose_name": "Objective",
        "short_name": "obj",
        "feature_type": "float",
    }


def init_data_feature_time_ms() -> dict[str, Any]:
    return {
        "name": "time_ms",
        "default": -1.0,
        "verbose_name": "Running Time (ms)",
        "short_name": "t_ms",
        "feature_type": "float",
    }


def init_default_problem_space() -> ProblemSpace:
    return ProblemSpace(
        name=_DEFAULT_PSPACE_NAME,
        run_key={
            "run_id": Feature(**init_data_feature_run_id()),
            "timestamp_added": Feature(**init_data_feature_timestamp_added()),
            "added_from": Feature(**init_data_feature_added_from()),
        },
        instance_key={
            "set_name": Feature(**init_data_feature_set_name()),
            "n": Feature(**init_data_feature_n()),
            "rep": Feature(**init_data_feature_rep()),
        },
        solver_key={"solver": Feature(**init_data_feature_solver())},
        output_key={
            "objective": Feature(**init_data_feature_objective()),
            "time_ms": Feature(**init_data_feature_time_ms()),
        },
        filepath=_DEFAULT_PSPACE_PATH,
    )


class TestSetup:
    def test_optiface_import(self):
        importlib.import_module("optiface")


class TestFeature:
    """
    Behaviors:
    - Feature class:
         - (init) initialize feature as expected when passed data with type(default) == feature_type.
         - (validation) raise (??) when passed data with type(default) != feature_type.
    """

    def test_feature_init(self):
        set_name_raw = init_data_feature_set_name()
        set_name = Feature(**set_name_raw)
        assert set_name.name == set_name_raw["name"]
        assert set_name.default == set_name_raw["default"]
        assert set_name.verbose_name == set_name_raw["verbose_name"]
        assert set_name.short_name == set_name_raw["short_name"]
        assert (
            set_name.feature_type == yaml_to_feature_type[set_name_raw["feature_type"]]
        )

    def test_feature_validation(self):
        with pytest.raises(RuntimeError):
            set_name_unknowntype_raw = init_data_feature_set_name_unknown_type()
            set_name_unknowntype = Feature(**set_name_unknowntype_raw)

        with pytest.raises(RuntimeError):
            set_name_mistyped_raw = init_data_feature_set_name_mistyped()
            set_name_mistyped = Feature(**set_name_mistyped_raw)


class TestProblemSpace:
    """
    Behaviors:
    - ProblemSpace class:
        - is read correctly from yaml, resulting in equivalent pspace instance to hardcoded test_pspace instance.
    """

    def test_defaultpspace_read(self):
        test_pspace = init_default_problem_space()
        read_pspace = read_pspace_from_yaml(name=_DEFAULT_PSPACE_NAME)
        assert test_pspace == read_pspace


class TestOptiSpace:
    """
    - start with just a list of problem names, managed by OSM

    Behaviors (ospace):
    - every problem name is correctly read, and filepath correctly constructed
    - every pspace:
        - (problemspace.yaml) every feature has a name (str), default (str), verbose_name (str), short_name (str), feature_type (type), default is of correct type
        - (problemspace.yaml <-> experiments.db match)
    """

    def test_ospace(self):
        ospace: OptiSpace = read_ospace()
        assert _DEFAULT_PSPACE_NAME in set(ospace.problems)

        for problem in ospace.problems:
            # ProblemSpace is a BaseModel, so pydantic checks its types (right Pete?).
            # We will still assert some types for excessive testing.

            # TODO: make sure that once you do OSM, switch current
            # ospace.current = problem
            pspace: ProblemSpace = read_pspace_from_yaml(problem)
            assert isinstance(pspace.name, str)
            assert pspace.name == problem
            assert isinstance(pspace.filepath, Path)

            for feature_name, feature in pspace.instance_key.items():
                assert isinstance(feature_name, str)
                assert feature_name == feature.name
                assert feature.feature_type is not None
                assert isinstance(feature.feature_type, type)
                assert feature.default is not None
                assert isinstance(feature.default, feature.feature_type)
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
