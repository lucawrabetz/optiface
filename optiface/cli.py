import sys
import platform
import pandas as pd

from typing import Callable
from pathlib import Path

from optiface.core.optierror import Status, StatusOr, Failure, Success

from optiface.core.optispace import (
    ProblemSpace,
    OptiSpace,
    OSpaceManager,
    read_pspace_from_yaml,
)

from optiface.dbmanager.dbm import AlchemyWAPI, init_alchemy_api

from optiface.constants import (
    _SPACE,
    _MIGRATIONS,
)

from rich.console import Console
from rich.prompt import Prompt


class OptiWizard:
    _HEADER_STYLE = "bold"
    _WARNING_STYLE = "bold red"
    _SUCCESS_STYLE = "bold green"
    _SUCCESS_2_STYLE = "bold cyan"
    _PROMPT_STYLE = "bold deep_pink3"
    _TAB = "  "
    _OPTIORANGE = "dark_orange3"
    _OPTIFACE = f"[bold {_OPTIORANGE}]optiface =][/bold {_OPTIORANGE}]"
    _EXIT_MSG = "\n[bold dark_orange3]exiting optiface =] goodbye![/bold dark_orange3]"

    _HOME = Path.cwd()
    _DBM = _HOME / "optiface/dbmanager/dbm.py"

    _SUCC_NOTES_FILES_TO_INTRO_MSG: dict[str, str] = {str(_DBM): "Database API"}
    _FAIL_ERRS_FILES_TO_INTRO_MSG: dict[str, str] = {str(_DBM): "Database API warnings"}
    _FAIL_NOTES_FILES_TO_INTRO_MSG: dict[str, str] = {str(_DBM): "Database API notes"}

    def __init__(self, console: Console = Console()):
        self.console = console
        self.console.clear()

    def header(self, msg: str) -> None:
        self.console.print(f"\n{msg}", style=self._HEADER_STYLE)

    def warning(self, msg: str) -> None:
        self.console.print(f"\n{msg}", style=self._WARNING_STYLE)

    def unwrap_failure(self, failure: StatusOr, print_notes=True) -> None:
        if failure.is_ok():
            raise ValueError("Passing success object to wizard.unwrap_failure!")

        title = failure.unwrap_title()
        if title == "":
            title = "Operation"
        self.warning(f"{title} failed with the following errors:")

        errors: dict[str, list[str]] = failure.unwrap_err()

        for file, errs in errors.items():
            if file in self._FAIL_ERRS_FILES_TO_INTRO_MSG:
                self.warning(self._FAIL_ERRS_FILES_TO_INTRO_MSG[file])
                for e in errs:
                    self.warning_list_item(e)

        if print_notes:
            notes: dict[str, list[str]] = failure.unwrap_notes()

            for file, note_list in notes.items():
                if file in self._FAIL_NOTES_FILES_TO_INTRO_MSG:
                    self.standard(self._FAIL_NOTES_FILES_TO_INTRO_MSG[file])
                    for n in note_list:
                        self.list_item(n)

    def unwrap_success(self, success: StatusOr, print_notes=True) -> None:
        if success.is_err():
            raise ValueError("Passing failure object to wizard.unwrap_success!")
        title = success.unwrap_title()
        if title == "":
            title = "Operation"

        self.success(f"{title} ended successfully!")
        if success.unwrap():
            self.success(f"Successfully unwrapped value {success.unwrap()}!")

        if print_notes:
            notes: dict[str, list[str]] = success.unwrap_notes()

            for file, note_list in notes.items():
                if file in self._SUCC_NOTES_FILES_TO_INTRO_MSG:
                    self.standard(self._SUCC_NOTES_FILES_TO_INTRO_MSG[file])
                    for n in note_list:
                        self.list_item(n)

    def warning_list_item(self, msg: str) -> None:
        self.console.print(f"{self._TAB}- {msg}", style=self._WARNING_STYLE)

    def list_item(self, msg: str) -> None:
        self.console.print(f"{self._TAB}- {msg}")

    def hl_list_item(self, msg: str) -> None:
        self.console.print(f"{self._TAB}* {msg} *", style=self._SUCCESS_STYLE)

    def kv_hl_list(self, msg_pairs: dict[str, str]) -> None:
        for k, v in msg_pairs.items():
            self.console.print(
                f"{self._TAB}[{self._SUCCESS_2_STYLE}]{k}:[/{self._SUCCESS_2_STYLE}] {v}"
            )

    def success(self, msg: str) -> None:
        self.console.print(f"\n{msg}", style=self._SUCCESS_STYLE)

    def standard(self, msg: str) -> None:
        self.console.print(f"\n{msg}")

    def string_input(self, prompt: str) -> str:
        return Prompt.ask(
            prompt=f"\n[{self._PROMPT_STYLE}]{prompt}[/{self._PROMPT_STYLE}]",
            console=self.console,
        )

    def choice_input(self, choices: list[str], prompt: str = "") -> str:
        return Prompt().ask(
            prompt=f"\n[{self._PROMPT_STYLE}] =] >>> {prompt}[/{self._PROMPT_STYLE}]",
            console=self.console,
            choices=choices,
            show_choices=True,
        )

    def yn_input(self, prompt: str) -> bool:
        return self.choice_input(choices=["y", "n"], prompt=prompt) == "y"

    def show_greeting(self):
        my_sys = platform.uname()
        self.console.line()
        self.console.rule(
            f"{self._OPTIFACE} running on {my_sys.system} at {my_sys.node}",
            style=self._OPTIORANGE,
        )

    def show_exit(self):
        self.console.print(f"{self._EXIT_MSG}\n")


class OptiFront:
    _CMD_DESCR: dict[str, str] = {
        "migrate": "Migrate data to a problem db",
        "new": "Create a new problem space",
        "switch": "Switch to an existing problem space",
        "status": "Show current status and available problem spaces",
        "help": "Show this help message",
        "exit": "Exit the application",
    }

    def __init__(self, wizard: OptiWizard):
        self.console = Console()
        self.wizard = wizard

        self._CMD: dict[str, Callable] = {
            "migrate": self.migrate_data,
            "new": self.new_pspace,
            "switch": self.switch_pspace,
            "status": self.show_status,
            "help": self.show_help,
            "exit": self.exit_optiface,
        }

        self._startup()
        self._read_ospace()

    def run(self) -> None:
        while True:
            choice = self.wizard.choice_input(list(self._CMD.keys()))
            self._CMD[choice]()

    def migrate_data(self) -> None:
        self.wizard.standard(
            f"Let's migrate some data! The active problemspace is: {self.osm.current_name}"
        )
        # add option to switch - add y/n function to wizardsuccess
        if self.wizard.yn_input("Would you like to switch first?"):
            self.switch_pspace()

        migration_dir: Path = _MIGRATIONS / self.osm.current_name

        self.wizard.standard(
            f"Please ensure that all your csv files are in {migration_dir}"
        )

        while not self.wizard.yn_input("Ready?"):
            pass

        for entry in migration_dir.iterdir():
            if entry.is_dir():
                self.wizard.standard(f"Skipping {entry}, it is a directory...")
                continue
            if not entry.is_file() or entry.suffix.lower() != ".csv":
                self.wizard.standard(f"Skipping {entry}, it is not a csv file...")
                continue

            if self.wizard.yn_input(f"Would you like to migrate csv file: {entry}?"):
                # consider who's responsible for error handling on problem space <-> dbschema <-> new csv data validation checks
                df = pd.read_csv(entry)

                if not self.alchemy_wapi:
                    self.wizard.warning(
                        "Uninitialized db api, problemspace was problably problematic. Please switch."
                    )
                    self.switch_pspace()
                    return

                status: Status = self.alchemy_wapi.insert_rows(df)

                if status.is_err():
                    self.wizard.unwrap_failure(failure=status)
                else:
                    self.wizard.unwrap_success(success=status)

        self.wizard.success("No more files to migrate -> All done!")

    def _handle_alchemy_res(
        self,
        res: StatusOr[AlchemyWAPI],
        succ_msg: str | None = None,
        show_status: bool = False,
    ) -> None:
        if res.is_err():
            self.wizard.unwrap_failure(res)
            raise RuntimeError("HOLD RuntimeError for unresolved error flow.")
            # could ask user to switch back to a problemspace that is not problematic?

        else:
            self.alchemy_wapi = res.unwrap()
            if succ_msg:
                self.wizard.success(succ_msg)
            if show_status:
                self.show_status()

    def new_pspace(self) -> None:
        name = self.wizard.string_input("What is the name of your problem?")

        if self.osm.problem_exists(name):
            self.wizard.warning(f"Problem {name} already exists!")
            return

        self.osm.add_new_pspace(name)

        alchemy_res: StatusOr[AlchemyWAPI] = init_alchemy_api(self.osm.current)

        self._handle_alchemy_res(alchemy_res, f"Created new problem {name}!")

    def switch_pspace(self) -> None:
        name = self.wizard.string_input(
            "Please type the problem you'd like to switch to:"
        )
        if not self.osm.problem_exists(name):
            self.wizard.warning(f"Problem {name} does not exist!")
            return

        self.wizard.success(f"Loading problem {name}...")
        self.osm.switch_current_pspace(name)
        alchemy_res: StatusOr[AlchemyWAPI] = init_alchemy_api(self.osm.current)
        self._handle_alchemy_res(alchemy_res, "Done!")

    def show_status(self):
        self.wizard.header("Available problem spaces:")

        current_name = self.osm.current.name

        for pname in self.osm.problems:
            if pname == current_name:
                self.wizard.hl_list_item(pname)
            else:
                self.wizard.list_item(pname)

    def show_help(self):
        self.wizard.header("Available commands:")

        self.wizard.kv_hl_list(self._CMD_DESCR)

    def exit_optiface(self):
        self.wizard.show_exit()
        sys.exit(0)

    def _startup(self) -> None:
        if set(self._CMD.keys()) != set(self._CMD_DESCR.keys()):
            raise RuntimeError(
                f"wizard <--> frontend commands are not aligned, check {__file__}"
            )

        if not _SPACE.exists():
            _SPACE.mkdir()

        if not _MIGRATIONS.exists():
            _MIGRATIONS.mkdir()

        self.wizard.show_greeting()

        return

    def _read_ospace(self) -> None:
        """
        OptiSpace discovery init / refresh.

        Db api tightly coupled with current pspace.
        """
        self.osm = OSpaceManager()

        for pname in self.osm.problems:
            migration_dir = _MIGRATIONS / pname

            if not migration_dir.exists():
                migration_dir.mkdir()

        alchemy_res: StatusOr[AlchemyWAPI] = init_alchemy_api(self.osm.current)
        self._handle_alchemy_res(alchemy_res)


def run():
    wizard = OptiWizard()
    of = OptiFront(wizard)
    of.run()


def main():
    pass


if __name__ == "__main__":
    main()
