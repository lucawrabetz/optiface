import os


from optiface import ui
from optiface.controller import experimentinterface
from optiface.core import iinstance
from optiface.datamodel import feature
from optiface.implementer import featureset
from optiface.implementer import instance

SPINE = featureset.optiface_init()
INSTANCE_KEY: feature.GroupKey = SPINE.instance_key
SOLVER_KEY: feature.GroupKey = SPINE.solver_key


def file_path_to_instance_id(file_path: str) -> feature.FeatureValueDict:
    # TODO: discuss naming - group keys, instance ids (without values vs with values, respectively).
    filename: str = os.path.split(file_path)[1].split(".")[0]
    parameters: list[str] = filename.split("_")
    if len(parameters) != len(INSTANCE_KEY):
        raise ValueError(f"Invalid file name: {filename}")
    instance_id: feature.FeatureValueDict = {}
    for i, (name, f) in enumerate(INSTANCE_KEY.items()):
        # TODO: stronger validation here than just casting?
        instance_id[name] = (f, f.feature_type(parameters[i]))
    return instance_id


def default_solver_id() -> feature.FeatureValueDict:
    return {k: (v, v.default) for k, v in SOLVER_KEY.items()}


def main() -> None:
    experiment = experimentinterface.ComputationalExperiment()
    instance_file_paths: list[str] = ["instances/test/test_2_0.csv"]
    pathid_pairs: list[feature.PathIdPair] = [
        (p, file_path_to_instance_id(p)) for p in instance_file_paths
    ]
    solver_ids: list[feature.FeatureValueDict] = [default_solver_id()]
    problem_instance: iinstance.IInstance = instance.PROBLEM_INSTANCE()
    experiment.configure(pathid_pairs, solver_ids, problem_instance)
    experiment.run()


if __name__ == "__main__":
    main()
