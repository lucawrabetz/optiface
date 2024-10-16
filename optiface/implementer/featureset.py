import yaml

from enum import Enum
from optiface import ui
from optiface import paths
from optiface.datamodel import feature
from typing import Type


# Implementer: define your enum types here:
# SolverType is required.
# Add any other enums you need here.
class SolverType(Enum):
    MySolver = "MySolver"


YML_FEATURE_TYPE_MAP: dict[str, Type] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "SolverType": SolverType,
}


# TODO: would like to move this class to optiface/datamodel/feature.py but it depends on SolverType which is here and should not be in datamodel/feature.py as it should be declared by the implementer. Ideally would like the SolverType enum to be encoded in the yaml file as well, so the implementer can add their solver types there. Not sure what the right way to do this is.
class FeatureSpine:
    def __init__(self) -> None:
        self.featureset: dict[str, feature.GroupKey] = {}

    def __str__(self) -> str:
        feature_set_summary = str()
        for group_name, group in self.featureset.items():
            feature_set_summary += f"\t{group_name}:\n"
            for _, feature in group.items():
                feature_set_summary += f"\t\t{feature.name}\n"
        return f"feature set:\n{feature_set_summary}"

    def read_yml(self, yml_path: str) -> None:
        # TODO: discuss validation better, when discussing layers and pydantic involvement.
        # - default values need to be validated
        with open(yml_path, "r") as file:
            yml_data = yaml.safe_load(file)

            for group_name, group_data in yml_data["featureset"].items():
                group: feature.GroupKey = {}
                for feature_name, feature_data in group_data.items():
                    feature_type: Type = YML_FEATURE_TYPE_MAP[
                        feature_data["feature_type"]
                    ]
                    new_feature = feature.Feature(
                        name=feature_name,
                        default=feature_type(feature_data["default"]),
                        feature_type=feature_type,
                        output_names=tuple(feature_data["output_names"]),
                    )
                    group[feature_name] = new_feature

                self.featureset[group_name] = group

    @property
    def instance_key(self) -> feature.GroupKey:
        return self.featureset["instance_key"]

    @property
    def solver_key(self) -> feature.GroupKey:
        return self.featureset["solver_key"]


FEATURE_SPINE = FeatureSpine()
FEATURE_SPINE.read_yml(paths.FEATURE_SET_YML_PATH)


def main() -> None:
    ui.body(FEATURE_SPINE.__str__())


if __name__ == "__main__":
    main()
