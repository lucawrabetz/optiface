"""
Run a "single experiment" - all solvers selected solving all instances selected.

Classes:

    ComputationalExperiment
"""
from optiface import ui
from optiface.core import iinstance
from optiface.core import isolution
from optiface.core import isolver
from optiface.datamodel import feature


class ComputationalExperiment:
    """
    Class to run a set of solvers on a set of instances.
    """

    def configure(
        self,
        instance_path_id_pairs: list[feature.PathIdPair],
        solver_ids: list[feature.FeatureValueDict],
        instance: iinstance.IInstance,
        solver: isolver.ISolver,
        solution: isolution.ISolution,
    ) -> None:
        """Configure experiment by setting attributes to store instance names and locations, and solver ids."""
        ui.header("Configuring Experiment [opti-face]")
        self._instance_path_id_pairs: list[feature.PathIdPair] = instance_path_id_pairs
        self._solver_ids: list[feature.FeatureValueDict] = solver_ids
        self._instance: iinstance.IInstance = instance
        self._solver: isolver.ISolver = solver
        self._solution: isolution.ISolution = solution

    def single_run(self, solver_id: feature.FeatureValueDict) -> None:
        """Solve a single instance with a single solver."""
        ui.body("In a single run [opti-face]...")
        solver_description: str = ", ".join([str(k[1]) for k in solver_id.values()])
        ui.separator_line()
        ui.body(
            f"Running {solver_description} on {self._instance.filepath} [opti-face]"
        )
        self._solver.configure(solver_id)
        self._solver.configure_from_instance(self._instance)
        self._solution = self._solver.solve()
        # TODO (LW): transfer to output row
        # TODO (LW + Integration): write output row to db
        self._solver.reset()
        self._solution.reset()

    def run(self) -> None:
        ui.subheader("Running an experiment [opti-face]...")
        for filepath, parameters in self._instance_path_id_pairs:
            self._instance.configure(parameters, filepath)
            self._instance.read()
            ui.separator_line()
            for solver_id in self._solver_ids:
                self.single_run(solver_id)
                self._instance.reset()
                ui.separator_line()
