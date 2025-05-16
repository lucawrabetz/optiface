from pathlib import Path
from sqlalchemy.util import OrderedProperties
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from collections import OrderedDict
from pydantic import BaseModel

from typing import Any, TypeAlias, TypeVar, Generic, Callable, Type

from optiface.core.featuredata import (
    init_data_feature_run_id,
    init_data_feature_timestamp_added,
    init_data_feature_added_from,
)

T = TypeVar("T")

_RUN_KEY_DATA = {
    "run_id": init_data_feature_run_id(),
    "timestamp_added": init_data_feature_timestamp_added(),
    "added_from": init_data_feature_added_from(),
}

_INSTANCE_KEY = "instance_key"
_SOLVER_KEY = "solver_key"
_OUTPUT_KEY = "output_key"

_SPACE: Path = Path("space")
_PS_FILE = "problemspace.yaml"

yaml_to_feature_type: dict[str, type] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "datetime": datetime,
    # keeping as str for now, but would probably like to tighten:
    #   - enums
}


def validate_str(s: str) -> bool:
    return isinstance(s, str)


def validate_int(x: int) -> bool:
    return isinstance(x, int)


def validate_float(x: float) -> bool:
    return isinstance(x, int) or isinstance(x, float)


def validate_bool(b: bool) -> bool:
    return isinstance(b, bool)


def validate_datetime(d: datetime) -> bool:
    return isinstance(d, datetime)


validate_allowed_types: dict[type, Callable[[Any], bool]] = {
    str: validate_str,
    int: validate_int,
    float: validate_float,
    bool: validate_bool,
    datetime: validate_datetime,
}


@dataclass
class Feature(Generic[T]):
    """
    Struct for a (results table) schema feature.

    TODO: is a feature_type: Type[T] (which requires str_to_type spines to read from yaml) useful? Starting without (where does validation come from)?
    TODO: unclear if Generic is necessary.
    """

    name: str
    required: bool
    default: T
    verbose_name: str
    short_name: str

    # would this be better annotated as Type[T]?
    # this actually is initialized as a string, and is then converted to a type in self.__post_init__
    feature_type_str: str
    feature_type: Type[T] = field(init=False)

    def __post_init__(self):
        # We can consider rolling our own exception (e.g. FeatureValidationError) as we go on here or using BaseModel and pydantic.ValidationError
        # Keeping prototype as simple as possible with RuntimeError for now

        # unknown type
        if self.feature_type_str not in yaml_to_feature_type.keys():
            raise RuntimeError(
                f"Feature {self.name} has unknown type {self.feature_type_str}"
            )

        self.feature_type = yaml_to_feature_type[self.feature_type_str]

        # required, but non-None default
        if self.required and self.default is not None:
            raise RuntimeError(
                f"Feature {self.name} is required, it should not have the default it currently has: {self.default}"
            )

        # not required, but no default
        if not self.required and self.default is None:
            raise RuntimeError(
                f"Feature {self.name} is not required, so it must have a default"
            )

        # wrong feature/default type
        if not self.required and not isinstance(self.default, self.feature_type):
            raise RuntimeError(
                f"Feature {self.name} has incorrect default type {type(self.default)}; it should be {self.feature_type}"
            )

        # names not strings
        if not isinstance(self.verbose_name, str):
            raise RuntimeError(
                f"Feature {self.name} has a verbose name of type {type(self.verbose_name)}"
            )

        # names not strings
        if not isinstance(self.short_name, str):
            raise RuntimeError(
                f"Feature {self.name} has a verbose name of type {type(self.verbose_name)}"
            )

    def __str__(self) -> str:
        return f"feature: {self.name}, feature_type: {self.feature_type}, required: {self.required}, default: {self.default}, output names: '{self.verbose_name}', '{self.short_name}'"


# 'Schema' type aliases
GroupKey: TypeAlias = OrderedDict[str, Feature]

# 'Row' type aliases
FeatureValuePair: TypeAlias = tuple[Feature, Any]


class ProblemSpace(BaseModel):
    name: str
    run_key: GroupKey
    instance_key: GroupKey
    solver_key: GroupKey
    output_key: GroupKey
    filepath: Path

    def print_features(self):
        print(f"pspace: {self.name}")
        for feature in self.run_key.values():
            print(feature)
        for feature in self.instance_key.values():
            print(feature)
        for feature in self.solver_key.values():
            print(feature)
        for feature in self.output_key.values():
            print(feature)

    def full_row_features_without_runkey(self) -> list[Feature]:
        return (
            list(self.instance_key.values())
            + list(self.solver_key.values())
            + list(self.output_key.values())
        )

    def validate_row(self, row: list[Any]) -> bool:
        # for now returns False if any incorrect cols encountered
        # replaces empty values with defaults in-place
        # empty value is recognized as None, not actually missing features in the list:
        # THIS DOES NOT INCLUDE THE RUN_KEY

        features = self.full_row_features_without_runkey()

        if len(row) < len(features):
            print(f"not valid: incomplete row")
            print([f.name for f in features])
            print(row)
            return False

        for i, value in enumerate(row):
            if not validate_allowed_types[features[i].feature_type](value):
                print(
                    f"type not valid for feature {features[i].name}, value is: {value}"
                )
                return False

        # TODO: we can't actually fully validate the row like this, we need row to arrive as a dict
        # if features[i].required:
        #     print(f"not valid: missing {features[i].name} which is required")
        #     return False
        # else:
        #     row[i] = features[i].default

        return True


@dataclass
class OptiSpace:
    problems: list[str]
    current: str


def process_key(data: dict[str, Any]) -> GroupKey:
    key: GroupKey = OrderedDict()

    for feature_name, feature_data in data.items():
        data_copy = feature_data
        data_copy["name"] = feature_name
        new_feature = Feature(**data_copy)
        key[feature_name] = new_feature
    return key


def read_pspace_from_yaml(name: str) -> ProblemSpace:
    """
    Factory for ProblemSpace:
        - in: problem name (e.g. testproblem, knapsack)
        - out: ProblemSpace object configured from space/<name>/problemspace.yaml
    """
    filepath: Path = Path(_SPACE) / name / _PS_FILE

    with open(filepath, "r") as file:
        yml_data = yaml.safe_load(file)
        run_key = process_key(_RUN_KEY_DATA)
        instance_key = process_key(yml_data[_INSTANCE_KEY])
        solver_key = process_key(yml_data[_SOLVER_KEY])
        output_key = process_key(yml_data[_OUTPUT_KEY])

    return ProblemSpace(
        name=name,
        run_key=run_key,
        instance_key=instance_key,
        solver_key=solver_key,
        output_key=output_key,
        filepath=filepath,
    )


def read_ospace() -> OptiSpace:
    """
    Factory for OptiSpace
    """
    problems: list[str] = []

    for entry in _SPACE.iterdir():
        if entry.is_dir():
            problems.append(entry.name)

    return OptiSpace(problems=problems, current=problems[0])
