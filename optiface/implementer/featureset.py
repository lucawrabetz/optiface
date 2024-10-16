import yaml

from enum import Enum
from optiface import ui
from optiface import paths
from optiface.datamodel import feature
from typing import Type, TypeAlias


class FeatureSpine:
    _SOLVER_TYPE_YML_PATH: str = paths.SOLVER_TYPE_YML_PATH
    _FEATURE_SET_YML_PATH = paths.FEATURE_SET_YML_PATH

    def __init__(self) -> None:
        self._featureset: dict[str, feature.GroupKey] = {}
        self._yml_to_feature_type: dict[str, Type] = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }

    def __str__(self) -> str:
        feature_set_summary = str()
        for group_name, group in self._featureset.items():
            feature_set_summary += f"\n\t{group_name}:"
            for _, feature in group.items():
                feature_set_summary += f"\n\t\t{feature.name}"
        return f"feature set:{feature_set_summary}"

    def read_yml_solvertype(self) -> None:
        with open(paths.SOLVER_TYPE_YML_PATH, "r") as file:
            solvertypes = yaml.safe_load(file)
        SolverType = Enum(
            "SolverType", {k: v for k, v in solvertypes["SolverType"].items()}
        )
        self._yml_to_feature_type["SolverType"] = SolverType

    def read_yml_featureset(self) -> None:
        # TODO: discuss validation better, when discussing layers and pydantic involvement.
        with open(self._FEATURE_SET_YML_PATH, "r") as file:
            yml_data = yaml.safe_load(file)

            for group_name, group_data in yml_data["featureset"].items():
                group: feature.GroupKey = {}
                for feature_name, feature_data in group_data.items():
                    feature_type: Type = self._yml_to_feature_type[
                        feature_data["feature_type"]
                    ]
                    new_feature = feature.Feature(
                        name=feature_name,
                        default=feature_type(feature_data["default"]),
                        feature_type=feature_type,
                        output_names=tuple(feature_data["output_names"]),
                    )
                    group[feature_name] = new_feature

                self._featureset[group_name] = group

    def configure_from_yml(self) -> None:
        self.read_yml_solvertype()
        self.read_yml_featureset()

    @property
    def instance_key(self) -> feature.GroupKey:
        return self._featureset["instance_key"]

    @property
    def solver_key(self) -> feature.GroupKey:
        return self._featureset["solver_key"]

    @property
    def feature_set(self) -> feature.FeatureValueDict:
        return self._featureset


def optiface_init() -> FeatureSpine:
    fs = FeatureSpine()
    fs.configure_from_yml()
    return fs


def main() -> None:
    fs = FeatureSpine()
    fs.configure_from_yml()
    ui.body(fs.__str__())


if __name__ == "__main__":
    main()
