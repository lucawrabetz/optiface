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
    OSpaceManager,
    yaml_to_feature_type,
    Feature,
    ProblemSpace,
    OptiSpace,
    read_pspace_from_yaml,
    init_default_problem_space,
)

from optiface.constants import _EXPERIMENTS_DBFILE, _SPACE, _PS_FILE, _DEFAULT

######### VERY IMPORTANT #########

# note: case insensitive conventions
# ProblemSpace, problemspace, PrOblemsPace are the same

# ProblemSpace - always refers to the ProblemSpace class
# pspace - refers to an arbitrary problem space

# OptiSpace - always refers to the OptiSpace class
# ospace - refers to this opti space

##################################


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
    # incorrect bc unknown type.
    return {
        "name": "set_name",
        "required": True,
        "default": None,
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "what_is_this_type",
    }


def init_data_feature_set_name_withdefault() -> dict[str, Any]:
    # incorrect bc shouldn't have default.
    return {
        "name": "set_name",
        "required": True,
        "default": "shouldntbehere",
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "str",
    }


def init_data_feature_timestamp_nodefault() -> dict[str, Any]:
    # incorrect bc should have default.
    return {
        "name": "timestamp_added",
        "required": False,
        "default": None,
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_featuretype_int() -> dict[str, Any]:
    # incorrect bc wrong type.
    return {
        "name": "timestamp_added",
        "required": False,
        "default": opti_dt.optidefault(),
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_intdefault() -> dict[str, Any]:
    # incorrect bc default is of wrong type.
    return {
        "name": "timestamp_added",
        "required": False,
        "default": 2,
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "datetime",
    }


def init_data_feature_time_ms_verbosenameint() -> dict[str, Any]:
    # incorrect bc verbose name should be a string.
    return {
        "name": "time_ms",
        "required": True,
        "default": None,
        "verbose_name": 1,
        "short_name": "t_ms",
        "feature_type_str": "float",
    }


def init_data_feature_time_ms_shortnameint() -> dict[str, Any]:
    # incorrect bc short name should be a string.
    return {
        "name": "time_ms",
        "required": True,
        "default": None,
        "verbose_name": "Running Time (ms)",
        "short_name": 1,
        "feature_type_str": "float",
    }


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
    ProblemSpace is an in-memory data-only python representation of the problem - instance, solvers, and outputs.

    Behaviors:
    - ProblemSpace class:
        - is read correctly from yaml, resulting in equivalent pspace instance to hardcoded test_pspace instance.
        - test validation functionality
            -
    """

    def test_read_pspace_from_yaml(self):
        default_pspace = init_default_problem_space()
        read_pspace = read_pspace_from_yaml()

        # excessive sanity checks
        assert isinstance(read_pspace.name, str)
        assert read_pspace.name == _DEFAULT

        for feature_name, feature in read_pspace.instance_key.items():
            assert isinstance(feature_name, str)
            assert feature_name == feature.name
            assert feature.feature_type is not None
            assert len(feature.verbose_name) > 0
            assert len(feature.short_name) > 0

        assert default_pspace == read_pspace

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


class TestOSpaceManager:
    """
    - OSpaceManager is a user <-> optispace API: so pspace yamls can stay locked and safe
        - read
            - every problem name is correctly read, and filepath correctly constructed
            - (problemspace.yaml <-> experiments.db match)
                - correct case (they match)
                - errors:
                    -
        - add new pspace
        - switch active pspace
        - add feature to pspace *
        - remove feature from pspace *
    - * includes dbmanager interaction (add or remove columns from databases)
    """

    _TEST_PSPACE_NAME: str = "testspace"

    def test_read(self):
        osm: OSpaceManager = OSpaceManager()
        assert _DEFAULT in set(osm.problems)

    def test_add_new_pspace(self):
        new_pspacedir: Path = _SPACE / self._TEST_PSPACE_NAME
        new_experimentsdb: Path = new_pspacedir / _EXPERIMENTS_DBFILE
        new_pspaceyaml: Path = new_pspacedir / _PS_FILE

        assert new_pspacedir.exists()
        assert new_experimentsdb.exists()
        assert new_pspaceyaml.exists()

    def test_pspace_switch(self):
        assert True

    def test_pspace_add_new_feature(self):
        assert True

    def test_pspace_remove_feature(self):
        assert True
