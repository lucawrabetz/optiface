import os
import yaml

from enum import Enum
from typing import Type

from optiface import ui
from optiface import paths
from optiface.datamodel import feature


class ProblemList:
    """
    Class to store all problems and solvers for each problem.
    Read from file optiface/var/enumtypes.yml.
    """

    def __init__(self) -> None:
        self._problem_dict: dict[str, list[tuple[str, str]]]
        self._problem_set_yml_path: str = os.path.join(
            paths._VAR_DIR, paths.ENUM_TYPE_FILE
        )

    def read_yml_problemset(self) -> None:
        # TODO: discuss validation better, when discussing layers and pydantic involvement.
        with open(self._problem_set_yml_path, "r") as file:
            yml_data = yaml.safe_load(file)

            for problem_name, solver_list in yml_data.items():

                new_list: list[tuple[str, str]] = []

                for solverclsname, solvername in solver_list:
                    new_list.append((solverclsname, solvername))

                self._problem_dict[problem_name] = new_list


class ProblemSpace:
    """
    Class to store feature spine for a single problem.
    """

    def __init__(self, problem_name: str) -> None:
        self._problem_name: str = problem_name
        self._feature_set_yml_path: str = os.path.join(
            paths._IMPLEMENTER_DIR, self._problem_name, paths.FEATURE_SET_FILE
        )
        self._featureset: dict[str, feature.GroupKey] = {}
        self._yml_to_feature_type: dict[str, Type] = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }
        self.read_yml_featureset()

    def __str__(self) -> str:
        feature_set_summary = str()
        for group_name, group in self._featureset.items():
            feature_set_summary += f"\n\t{group_name}:"
            for _, feature in group.items():
                feature_set_summary += f"\n\t\t{feature.name}"
        return f"feature set:{feature_set_summary}"

    def read_yml_featureset(self) -> None:
        # TODO: discuss validation better, when discussing layers and pydantic involvement.
        with open(self._feature_set_yml_path, "r") as file:
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

    @property
    def instance_key(self) -> feature.GroupKey:
        return self._featureset["instance_key"]

    @property
    def solver_key(self) -> feature.GroupKey:
        return self._featureset["solver_key"]

    @property
    def feature_set(self) -> feature.FeatureValueDict:
        return self._featureset


def main() -> None:
    problem_name: str = "knapsack"

    fs = ProblemSpace(problem_name)
    fs.configure_from_yml()
    ui.body(fs.__str__())


if __name__ == "__main__":
    main()
