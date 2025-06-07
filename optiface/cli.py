import os
import sys
import platform

from typing import Callable
from pathlib import Path


from optiface.core.optispace import (
    ProblemSpace,
    OptiSpace,
    OSpaceManager,
    read_pspace_from_yaml,
)

from optiface.dbmanager.dbm import AlchemyWAPI, init_alchemy_api

from optiface.constants import (
    _SPACE,
    _PS_FILE,
    opti_user_data_dir,
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

    def __init__(self, console: Console = Console()):
        self.console = console
        self.console.clear()

    def header(self, msg: str) -> None:
        self.console.print(f"\n{msg}", style=self._HEADER_STYLE)

    def warning(self, msg: str) -> None:
        self.console.print(f"\n{msg}", style=self._WARNING_STYLE)

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
        self.console.print(msg)

    def string_input(self, prompt: str) -> str:
        return Prompt.ask(
            prompt=f"\n[{self._PROMPT_STYLE}]{prompt}[/{self._PROMPT_STYLE}]",
            console=self.console,
        )

    def choice_input(self, choices: list[str]) -> str:
        return Prompt().ask(
            prompt=f"\n[{self._PROMPT_STYLE}] =] >>>[/{self._PROMPT_STYLE}]",
            console=self.console,
            choices=choices,
            show_choices=True,
        )

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

    def new_pspace(self) -> None:
        name = self.wizard.string_input("what is the name of your problem?")

        if self.osm.problem_exists(name):
            self.wizard.warning(f"Problem {name} already exists!")
            return

        self.osm.add_new_pspace(name)
        self.alchemy_wapi = init_alchemy_api(self.osm.current)

        self.wizard.success(f"Created new problem {name}!")
        self.show_status()

    def switch_pspace(self) -> None:
        name = self.wizard.string_input(
            "Please type the problem you'd like to switch to:"
        )
        if not self.osm.problem_exists(name):
            self.wizard.warning(f"Problem {name} does not exist!")
            return

        self.wizard.success(f"Loading problem {name}...")
        self.osm.switch_current_pspace(name)
        self.alchemy_wapi = init_alchemy_api(self.osm.current)
        self.wizard.success("Done!")

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
        # sanity checks
        if set(self._CMD.keys()) != set(self._CMD_DESCR.keys()):
            raise RuntimeError(
                f"wizard <--> frontend commands are not aligned, check {__file__}"
            )

        self.wizard.show_greeting()

        return

    def _read_ospace(self) -> None:
        """
        OptiSpace discovery init / refresh.

        Db api tightly coupled with current pspace.
        """
        self.osm = OSpaceManager()
        self.alchemy_wapi = init_alchemy_api(self.osm.current)


def run():
    wizard = OptiWizard()
    of = OptiFront(wizard)
    of.run()


def main():
    pass


if __name__ == "__main__":
    main()
