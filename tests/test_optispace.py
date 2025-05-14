import importlib
import pytest

from pathlib import Path
from typing import Any
from optiface.core.featuredata import (
    init_data_feature_run_id,
    init_data_feature_timestamp_added,
    init_data_feature_added_from,
)
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


def init_data_feature_set_name() -> dict[str, Any]:
    return {
        "name": "set_name",
        "required": True,
        "default": None,
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "str",
    }


def init_data_feature_set_name_unknown_type() -> dict[str, Any]:
    return {
        "name": "set_name",
        "required": True,
        "default": None,
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "what_is_this_type",
    }


def init_data_feature_set_name_withdefault() -> dict[str, Any]:
    return {
        "name": "set_name",
        "required": True,
        "default": "shouldntbehere",
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "str",
    }


def init_data_feature_timestamp_nodefault() -> dict[str, Any]:
    return {
        "name": "timestamp_added",
        "required": False,
        "default": None,
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_featuretype_int() -> dict[str, Any]:
    return {
        "name": "timestamp_added",
        "required": False,
        "default": opti_dt.optidefault(),
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_intdefault() -> dict[str, Any]:
    return {
        "name": "timestamp_added",
        "required": False,
        "default": 2,
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "datetime",
    }


def init_data_feature_n() -> dict[str, Any]:
    return {
        "name": "n",
        "required": True,
        "default": None,
        "verbose_name": "Number of Items",
        "short_name": "n",
        "feature_type_str": "int",
    }


def init_data_feature_rep() -> dict[str, Any]:
    return {
        "name": "rep",
        "required": False,
        "default": 0,
        "verbose_name": "Instance Rep",
        "short_name": "i_rep",
        "feature_type_str": "int",
    }


# TODO: unclear to me whether str is enough as solver "uuid" or if a solver id class is helpful
def init_data_feature_solver() -> dict[str, Any]:
    return {
        "name": "solver",
        "required": True,
        "default": None,
        "verbose_name": "Solver",
        "short_name": "sol",
        "feature_type_str": "str",
    }


def init_data_feature_objective() -> dict[str, Any]:
    return {
        "name": "objective",
        "required": True,
        "default": None,
        "verbose_name": "Objective",
        "short_name": "obj",
        "feature_type_str": "float",
    }


def init_data_feature_time_ms() -> dict[str, Any]:
    return {
        "name": "time_ms",
        "required": True,
        "default": None,
        "verbose_name": "Running Time (ms)",
        "short_name": "t_ms",
        "feature_type_str": "float",
    }


def init_data_feature_time_ms_verbosenameint() -> dict[str, Any]:
    return {
        "name": "time_ms",
        "required": True,
        "default": None,
        "verbose_name": 1,
        "short_name": "t_ms",
        "feature_type_str": "float",
    }


def init_data_feature_time_ms_shortnameint() -> dict[str, Any]:
    return {
        "name": "time_ms",
        "required": True,
        "default": None,
        "verbose_name": "Running Time (ms)",
        "short_name": 1,
        "feature_type_str": "float",
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
         - (init) initialize feature as expected when passed data with type(default) == feature_type_str.
         - (validation)
            - raise (??) when passed data with an unknown type.
            - raise (??) when passed data with required == True and default != null.
            - raise (??) when passed data with required == False and default == null.
            - raise (??) when passed data with required == False and type(default) != yaml_to_feature_type[feature_type_str].
            - raise (??) when passed data with type(short_name) != str or type(verbose_name) != str.
    """

    def test_feature_init(self):
        set_name_raw = init_data_feature_set_name()
        set_name = Feature(**set_name_raw)
        assert set_name.name == set_name_raw["name"]
        assert set_name.default == set_name_raw["default"]
        assert set_name.verbose_name == set_name_raw["verbose_name"]
        assert set_name.short_name == set_name_raw["short_name"]
        assert (
            set_name.feature_type
            == yaml_to_feature_type[set_name_raw["feature_type_str"]]
        )

    def test_feature_validation(self):
        # unknown type
        with pytest.raises(RuntimeError):
            set_name_unknowntype_raw = init_data_feature_set_name_unknown_type()
            set_name_unknowntype = Feature(**set_name_unknowntype_raw)

        # required, but non-None default
        with pytest.raises(RuntimeError):
            set_name_with_default_raw = init_data_feature_set_name_withdefault()
            set_name_with_default = Feature(**set_name_with_default_raw)

        # not required, but no default
        with pytest.raises(RuntimeError):
            timestamp_nodefault_raw = init_data_feature_timestamp_nodefault()
            timestamp_nodefault = Feature(**timestamp_nodefault_raw)

        # wrong feature type
        with pytest.raises(RuntimeError):
            timestamp_featuretype_int_raw = (
                init_data_feature_timestamp_featuretype_int()
            )
            timestamp_featuretype_int = Feature(**timestamp_featuretype_int_raw)

        # wrong default type
        with pytest.raises(RuntimeError):
            timestamp_intdefault_raw = init_data_feature_timestamp_intdefault()
            timestamp_intdefault = Feature(**timestamp_intdefault_raw)

        # non-string verbose name
        with pytest.raises(RuntimeError):
            time_ms_verboseint_raw = init_data_feature_time_ms_verbosenameint()
            time_ms_verboseint = Feature(**time_ms_verboseint_raw)

        # non-string short name
        with pytest.raises(RuntimeError):
            time_ms_shortint_raw = init_data_feature_time_ms_shortnameint()
            time_ms_shortint = Feature(**time_ms_shortint_raw)


def correct_default_row_one_empty() -> list[Any]:
    return ["defaultset", 1, None, "MIP", 100, 100]


def incorrect_types_default_row() -> list[Any]:
    return ["defaultset", "one", None, "MIP", 100, 100]


def incorrect_missing_required_default_row() -> list[Any]:
    return ["defaultset", None, None, "MIP", 100, 100]


class TestProblemSpace:
    """
    Behaviors:
    - ProblemSpace class:
        - is read correctly from yaml, resulting in equivalent pspace instance to hardcoded test_pspace instance.
        - all features pass validation checks
    """

    def test_defaultpspace_read(self):
        test_pspace = init_default_problem_space()
        read_pspace = read_pspace_from_yaml(name=_DEFAULT_PSPACE_NAME)
        assert test_pspace == read_pspace

    def test_validate_correct_row(self):
        default_pspace = init_default_problem_space()
        default_row = correct_default_row_one_empty()
        valid = default_pspace.validate_row(default_row)

        assert valid
        assert default_row[2] == default_pspace.instance_key["rep"].default

    def test_validate_row_incorrect_types(self):
        default_pspace = init_default_problem_space()
        default_row = incorrect_types_default_row()

        valid = default_pspace.validate_row(default_row)

        assert not valid

    def test_validate_row_missing_required(self):
        default_pspace = init_default_problem_space()
        default_row = incorrect_missing_required_default_row()

        valid = default_pspace.validate_row(default_row)

        assert not valid


class TestOptiSpace:
    """
    - start with just a list of problem names, managed by OSM

    Behaviors (ospace):
    - every problem name is correctly read, and filepath correctly constructed
    - every pspace:
        - (problemspace.yaml) every feature passes validation, some sanity checks for now
                (covered in TestFeature.test_validation)
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
                assert len(feature.verbose_name) > 0
                assert len(feature.short_name) > 0


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
