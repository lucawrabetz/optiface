import logging

from optiface import ui
from pydantic import BaseModel
from typing import Any, Type, TypeAlias

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


OutputNames: TypeAlias = tuple[str, str]


class Feature(BaseModel):
    """
    Struct for a schema feature.
    """

    # TODO: at this point defining Feature, while using pydantic and BaseModel, is a huge code smell to me.
    # The main reason I am defining Feature as a BaseModel is because we can use pydantic's create_model to add Features dynamically on the optiface side, when this happens on the database side.
    # However, it seems to me that everything in Feature is already defined in pydantic's Field, then the whole "FeatureSet" or "Row of ResultsTable" could be a pydantic BaseModel.
    _PRETTY_IDX: int = 0
    _SHORT_IDX: int = 1
    name: str
    default: Any
    feature_type: Type
    output_names: OutputNames

    def __str__(self) -> str:
        return f"feature: {self.name}, type: {self.feature_type}, default: {self.default}, output name: {self.pretty} [{self.short}]"

    @property
    def pretty(self) -> str:
        return self.output_names[self._PRETTY_IDX]

    @property
    def short(self) -> str:
        return self.output_names[self._SHORT_IDX]


# TODO: shoud we restrict Any to be a union of possible types? This is probably unnecessary but let's revisit...
GroupKey: TypeAlias = dict[str, Feature]
FeatureValuePair: TypeAlias = tuple[Feature, Any]
FeatureValueDict: TypeAlias = dict[str, FeatureValuePair]
PathIdPair: TypeAlias = tuple[str, FeatureValueDict]


def main() -> None:
    feature_data: dict[str, Any] = {
        "name": "set_name",
        "default": "test",
        "feature_type": str,
        "output_names": ("Set Name", "s_n"),
    }
    SET_NAME = Feature(**feature_data)
    ui.header("Declaring a feature")
    ui.subheader("Set Name Example Feature")
    ui.body(SET_NAME.__str__())


if __name__ == "__main__":
    main()
