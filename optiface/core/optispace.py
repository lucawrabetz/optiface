from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, Type, TypeAlias


@dataclass
class Feature:
    """
    Struct for a problem results schema feature.
    """

    name: str
    feature_type: Type
    default: Any
    verbose_name: str
    short_name: str

    def __str__(self) -> str:
        return f"feature: {self.name}, type: {self.feature_type}, default: {self.default}, output names: '{self.verbose_name}', '{self.short_name}'"


# TODO: shoud we restrict Any to be a union of possible types? This is probably unnecessary but let's revisit...
GroupKey: TypeAlias = dict[str, Feature]
FeatureValuePair: TypeAlias = tuple[Feature, Any]
FeatureValueDict: TypeAlias = dict[str, FeatureValuePair]
PathIdPair: TypeAlias = tuple[str, FeatureValueDict]


class ProblemSpace(BaseModel):
    pass
