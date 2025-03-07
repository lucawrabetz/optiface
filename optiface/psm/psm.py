from optiface.core.optispace import (
    Feature,
    ProblemSpace,
    OptiSpace,
    read_ps_from_yaml,
    read_optispace,
)


class PSM:
    def __init__(self):
        self.optispace: OptiSpace = read_optispace()
        self.wizard: OptiWizard = get_wizard()

    def ps_factory(self) -> ProblemSpace:
        return ProblemSpace(
            name="bleah",
            instance_key=dict(),
            solver_key=dict(),
            outputs=dict(),
            filepath="bleah",
        )
