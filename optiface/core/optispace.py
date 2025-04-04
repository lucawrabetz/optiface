from pathlib import Path
import yaml
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel

from typing import Any, TypeAlias, TypeVar, Generic

T = TypeVar("T")

_RUN_KEY = "run_key"
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
    #   - datetime
    #   - enums
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
    feature_type: type

    def __post_init__(self):
        # We can consider rolling our own exception (e.g. FeatureValidationError) as we go on here or using BaseModel and pydantic.ValidationError
        # Keeping prototype as simple as possible with RuntimeError for now

        if self.feature_type not in yaml_to_feature_type.keys():
            raise RuntimeError(
                f"Feature {self.name} has unknown type {self.feature_type}"
            )

        self.feature_type = yaml_to_feature_type[self.feature_type]

        if not self.required and not isinstance(self.default, self.feature_type):
            raise RuntimeError(
                f"Feature {self.name} has incorrect default type {type(self.default)}; it should be {self.feature_type}"
            )

    def __str__(self) -> str:
        return f"feature: {self.name}, feature_type: {self.feature_type}, default: {self.default}, type_of_default: {type(self.default)}, output names: '{self.verbose_name}', '{self.short_name}'"


# 'Schema' type aliases
GroupKey: TypeAlias = dict[str, Feature]

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


@dataclass
class OptiSpace:
    problems: list[str]
    current: str


def process_key(data: dict[str, Any]) -> GroupKey:
    key: GroupKey = dict()
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
    run_key: GroupKey = dict()
    instance_key: GroupKey = dict()
    solver_key: GroupKey = dict()
    outputs: GroupKey = dict()

    with open(filepath, "r") as file:
        yml_data = yaml.safe_load(file)
        run_key = process_key(yml_data[_RUN_KEY])
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
