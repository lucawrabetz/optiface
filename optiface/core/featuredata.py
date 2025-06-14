from typing import Any

_RUN_KEY = "run_key"
_INSTANCE_KEY = "instance_key"
_SOLVER_KEY = "solver_key"
_OUTPUT_KEY = "output_key"

_REQUIRED = "required"
_DEFAULT = "default"
_VERBOSE_NAME = "verbose_name"
_SHORT_NAME = "short_name"
_FEATURE_TYPE_STR = "feature_type_str"
_FEATURE_TYPE = "feature_type"


_RUN_ID = "run_id"
_TIMESTAMP_ADDED = "timestamp_added"
_ADDED_FROM = "added_from"


def init_data_feature_run_id() -> dict[str, Any]:
    return {
        "name": _RUN_ID,
        "required": True,
        "default": None,
        "verbose_name": "Run Id",
        "short_name": "run_id",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_added() -> dict[str, Any]:
    return {
        "name": _TIMESTAMP_ADDED,
        "required": True,
        "default": None,
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "datetime",
    }


def init_data_feature_added_from() -> dict[str, Any]:
    return {
        "name": _ADDED_FROM,
        "required": True,
        "default": None,
        "verbose_name": "Added From",
        "short_name": "from",
        "feature_type_str": "str",
    }


_RUN_KEY_FDATA = {
    _RUN_ID: init_data_feature_run_id(),
    _TIMESTAMP_ADDED: init_data_feature_timestamp_added(),
    _ADDED_FROM: init_data_feature_added_from(),
}

_SET_NAME = "set_name"
_REP = "rep"


def init_data_feature_set_name() -> dict[str, Any]:
    return {
        "name": _SET_NAME,
        "required": True,
        "default": None,
        "verbose_name": "Set Name",
        "short_name": "s_n",
        "feature_type_str": "str",
    }


def init_data_feature_rep() -> dict[str, Any]:
    return {
        "name": _REP,
        "required": False,
        "default": 0,
        "verbose_name": "Instance Rep",
        "short_name": "i_rep",
        "feature_type_str": "int",
    }


_DEFAULT_INSTANCE_KEY_FDATA = {
    _SET_NAME: init_data_feature_set_name(),
    _REP: init_data_feature_rep(),
}

_SOLVER = "solver"


# TODO: unclear to me whether str is enough as solver "uuid" or if a solver id class is helpful
def init_data_feature_solver() -> dict[str, Any]:
    return {
        "name": _SOLVER,
        "required": True,
        "default": None,
        "verbose_name": "Solver",
        "short_name": "sol",
        "feature_type_str": "str",
    }


_DEFAULT_SOLVER_KEY_FDATA = {_SOLVER: init_data_feature_solver()}

_OBJECTIVE = "objective"
_TIME_MS = "time_ms"


def init_data_feature_objective() -> dict[str, Any]:
    return {
        "name": _OBJECTIVE,
        "required": True,
        "default": None,
        "verbose_name": "Objective",
        "short_name": "obj",
        "feature_type_str": "float",
    }


def init_data_feature_time_ms() -> dict[str, Any]:
    return {
        "name": _TIME_MS,
        "required": True,
        "default": None,
        "verbose_name": "Running Time (ms)",
        "short_name": "t_ms",
        "feature_type_str": "float",
    }


_DEFAULT_OUTPUT_KEY_FDATA = {
    _OBJECTIVE: init_data_feature_objective(),
    _TIME_MS: init_data_feature_time_ms(),
}
