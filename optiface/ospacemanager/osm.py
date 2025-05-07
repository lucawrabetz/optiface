from optiface.core.optispace import (
    Feature,
    ProblemSpace,
    OptiSpace,
    read_pspace_from_yaml,
    read_ospace,
)


class OSM:
    def __init__(self):
        self.ospace: OptiSpace = read_ospace()
        # self.wizard: OptiWizard = get_wizard()

    def create_new_pspace(self, name: str) -> ProblemSpace:
        # write a new default problemspace.yaml file
        return read_pspace_from_yaml(name)

    def switch_current_pspace(self, name: str) -> ProblemSpace:
        if name not in set(self.ospace.problems):
            return read_pspace_from_yaml(self.ospace.current)
        else:
            self.ospace.current = name
            return read_pspace_from_yaml(name)
