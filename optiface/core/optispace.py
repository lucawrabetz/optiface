from pathlib import Path
import yaml
from dataclasses import dataclass
from pydantic import BaseModel

from typing import Any, TypeAlias, TypeVar, Generic

T = TypeVar("T")

_SPACE: Path = Path("space")
_PS_FILE = "problemspace.yaml"


@dataclass
class Feature(Generic[T]):
    """
    Struct for a (results table) schema feature.

    TODO: is a feature_type: Type[T] (which requires str_to_type spines to read from yaml) useful? Starting without (where does validation come from)?
    TODO: unclear if Generic is necessary.
    """

    name: str
    default: T
    verbose_name: str
    short_name: str

    def __str__(self) -> str:
        return f"feature: {self.name}, type: {type(self.default)}, default: {self.default}, output names: '{self.verbose_name}', '{self.short_name}'"


# 'Schema' type aliases
GroupKey: TypeAlias = dict[str, Feature]

# 'Row' type aliases
FeatureValuePair: TypeAlias = tuple[Feature, Any]


class ProblemSpace(BaseModel):
    name: str
    instance_key: GroupKey
    solver_key: GroupKey
    outputs: GroupKey
    filepath: Path


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
    filepath = Path(_SPACE) / name / _PS_FILE
    instance_key: GroupKey = dict()
    solver_key: GroupKey = dict()
    outputs: GroupKey = dict()

    with open(filepath, "r") as file:
        yml_data = yaml.safe_load(file)
        instance_key = process_key(yml_data["instance_key"])
        solver_key = process_key(yml_data["solver_key"])
        outputs = process_key(yml_data["outputs"])

    return ProblemSpace(
        name=name,
        instance_key=instance_key,
        solver_key=solver_key,
        outputs=outputs,
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
