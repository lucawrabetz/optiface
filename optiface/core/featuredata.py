from typing import Any
from optiface.core.optidatetime import OptiDateTimeFactory

opti_dt = OptiDateTimeFactory()


def init_data_feature_run_id() -> dict[str, Any]:
    return {
        "name": "run_id",
        "required": True,
        "default": None,
        "verbose_name": "Run Id",
        "short_name": "run_id",
        "feature_type_str": "int",
    }


def init_data_feature_timestamp_added() -> dict[str, Any]:
    return {
        "name": "timestamp_added",
        "required": False,
        "default": opti_dt.optidefault(),
        "verbose_name": "Timestamp Added",
        "short_name": "ts_added",
        "feature_type_str": "datetime",
    }


def init_data_feature_added_from() -> dict[str, Any]:
    return {
        "name": "added_from",
        "required": False,
        "default": "RUN",
        "verbose_name": "Added From",
        "short_name": "from",
        "feature_type_str": "str",
    }
