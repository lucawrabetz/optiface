from pathlib import Path
from sqlalchemy.util import OrderedProperties
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel

from typing import Any, TypeAlias, TypeVar, Generic, Callable, Type

from optiface.core.optidatetime import OptiDateTimeFactory

from optiface.core.optierror import Status, Success, Failure


from optiface.core.featuredata import (
    _TIMESTAMP_ADDED,
    _ADDED_FROM,
    _RUN_KEY_FDATA,
    _DEFAULT_INSTANCE_KEY_FDATA,
    _DEFAULT_SOLVER_KEY_FDATA,
    _DEFAULT_OUTPUT_KEY_FDATA,
    _INSTANCE_KEY,
    _SOLVER_KEY,
    _OUTPUT_KEY,
    _REQUIRED,
    _DEFAULT,
    _VERBOSE_NAME,
    _SHORT_NAME,
    _FEATURE_TYPE_STR,
)

T = TypeVar("T")


from optiface.constants import (
    _SPACE,
    _PS_FILE,
    _DEFAULT,
    _EXPERIMENTS_DBFILE,
    check_make_dir,
    copy_dir,
)


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

    def raw_dict(self) -> dict[str, Any]:
        return {
            _REQUIRED: self.required,
            _DEFAULT: self.default,
            _VERBOSE_NAME: self.verbose_name,
            _SHORT_NAME: self.short_name,
            _FEATURE_TYPE_STR: self.feature_type_str,
        }


# 'Row' type aliases
FeatureValuePair: TypeAlias = tuple[Feature, Any]


odtf = OptiDateTimeFactory()


class ProblemSpace(BaseModel):
    name: str
    instance_key: dict[str, Feature]
    solver_key: dict[str, Feature]
    output_key: dict[str, Feature]

    def print_features(self):
        print(f"pspace: {self.name}")
        for feature in _RUN_KEY_FDATA.values():
            print(feature)
        for feature in self.instance_key.values():
            print(feature)
        for feature in self.solver_key.values():
            print(feature)
        for feature in self.output_key.values():
            print(feature)

    def raw_feature_data(self) -> dict[str, dict[str, dict[str, str]]]:
        instance_key = {k: v.raw_dict() for k, v in self.instance_key.items()}
        solver_key = {k: v.raw_dict() for k, v in self.solver_key.items()}
        output_key = {k: v.raw_dict() for k, v in self.output_key.items()}
        return {
            _INSTANCE_KEY: instance_key,
            _SOLVER_KEY: solver_key,
            _OUTPUT_KEY: output_key,
        }

    def write_to_yaml(self) -> None:
        space_dir: Path = _SPACE / self.name

        if not space_dir.exists():
            space_dir.mkdir()

        yaml_file: Path = space_dir / _PS_FILE

        # TODO: take run_key off the problemspace class
        yaml_data: dict[str, dict[str, dict[str, str]]] = self.raw_feature_data()

        with open(yaml_file, "w") as file:
            yaml.safe_dump(yaml_data, file)

        return

    def full_row(self) -> list[Feature]:
        return (
            list(self.instance_key.values())
            + list(self.solver_key.values())
            + list(self.output_key.values())
        )

    def add_run_key(self, row: dict[str, Any]) -> None:
        # not run_id, as it is a primary_key, handled by sqlalchemy
        row[_TIMESTAMP_ADDED] = odtf.optinow()
        # can only migrate from csv for now
        row[_ADDED_FROM] = "CSV"

    def validate_row(self, row: dict[str, Any]) -> Status:
        # Sanitizes the row in-place with defaults.
        # TODO: skipping of run_key features? Extra unexpected features?

        features: list[Feature] = self.full_row()

        failure: Failure[None] = Failure(title="Row validation")

        fset = set([f.name for f in features])

        for f in features:
            # if the row contains a value for the feature, it must be of the correct type
            if f.name in row.keys() and row[f.name] is not None:
                if not validate_allowed_types[f.feature_type](row[f.name]):
                    failure.add_err(
                        err=f"type not valid for feature {f.name}, value is: {row[f.name]}",
                        file=__file__,
                    )

            # if feature is required, it must be found in the row
            else:
                if f.required:
                    failure.add_err(
                        err=f"missing feature {f.name} which is required", file=__file__
                    )
                else:
                    row[f.name] = f.default

            # result: f was either found in the row or it was not required and we added it

        if failure.has_errs:
            return failure

        # input row had all required features, now also filled in with defaults for missing
        # non-required features
        success: Success[None] = Success(value=None, title="Row validation")

        # add notes for extraneous features if they existed, remove them from row
        remove: list[str] = []
        for c in row.keys():
            if c not in fset:
                note: str = f"additional column {c} with value {row[c]} ignored"
                success.add_note(note, __file__)
                remove.append(c)

        for c in remove:
            del row[c]

        return success


@dataclass
class OptiSpace:
    problems: list[str]
    current: ProblemSpace


def process_key(data: dict[str, Any]) -> dict[str, Feature]:
    key = dict()

    for feature_name, feature_data in data.items():
        data_copy = feature_data
        data_copy["name"] = feature_name
        new_feature = Feature(**data_copy)
        key[feature_name] = new_feature

    return key


def run_key_features() -> dict[str, Feature]:
    return process_key(_RUN_KEY_FDATA)


def init_default_problem_space(name: str = _DEFAULT) -> ProblemSpace:
    instance_key = process_key(_DEFAULT_INSTANCE_KEY_FDATA)
    solver_key = process_key(_DEFAULT_SOLVER_KEY_FDATA)
    output_key = process_key(_DEFAULT_OUTPUT_KEY_FDATA)

    return ProblemSpace(
        name=name,
        instance_key=instance_key,
        solver_key=solver_key,
        output_key=output_key,
    )


def read_pspace_from_yaml(name: str = _DEFAULT) -> ProblemSpace:
    """
    Factory for ProblemSpace (read from existing yaml config file):
        - in: problem name (e.g. testproblem, knapsack)
        - out: ProblemSpace object configured from space/<name>/problemspace.yaml
    """
    filepath: Path = _SPACE / name / _PS_FILE

    with open(filepath, "r") as file:
        yml_data = yaml.safe_load(file)
        instance_key = process_key(yml_data[_INSTANCE_KEY])
        solver_key = process_key(yml_data[_SOLVER_KEY])
        output_key = process_key(yml_data[_OUTPUT_KEY])

    return ProblemSpace(
        name=name,
        instance_key=instance_key,
        solver_key=solver_key,
        output_key=output_key,
    )


class OSpaceManager:
    def __init__(self):
        self.read()

    @property
    def current(self) -> ProblemSpace:
        return self.ospace.current

    @property
    def current_name(self) -> str:
        return self.ospace.current.name

    @property
    def problems(self) -> list[str]:
        return self.ospace.problems

    def problem_exists(self, name: str) -> bool:
        return name in set(self.ospace.problems)

    def read(self) -> None:
        problems: list[str] = []

        for entry in _SPACE.iterdir():
            if entry.is_dir():
                problems.append(entry.name)

        if problems == []:
            self.ospace = OptiSpace(
                problems=[_DEFAULT], current=init_default_problem_space(name=_DEFAULT)
            )
            self.ospace.current.write_to_yaml()
            return

        current_pspace = read_pspace_from_yaml(problems[0])
        self.ospace = OptiSpace(problems=problems, current=current_pspace)

    def add_new_pspace(self, name: str) -> None:
        """
        TODO easy additions (GFI):
            - immediately add new custom features when creating (work with wizard)
        """
        self.ospace.current = init_default_problem_space(name)
        self.ospace.current.write_to_yaml()
        self.problems.append(name)

    def switch_current_pspace(self, name: str) -> None:
        self.ospace.current = read_pspace_from_yaml(name)
