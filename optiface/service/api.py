from abc import ABC, abstractmethod
import curses
from typing import Any, Generic, TypeVar, Sequence

ValType = TypeVar("ValType")


class IOView(ABC, Generic[ValType]):
    @abstractmethod
    def push(self, val: ValType) -> None:
        pass

    @abstractmethod
    def pull(self) -> Sequence[ValType]:
        pass


class ServiceAdaptor(ABC, Generic[ValType]):
    def __init__(self, input_view: IOView[ValType], output_view: IOView[ValType]):
        self._input_view = input_view
        self._output_view = output_view

    def push(self, val: ValType) -> None:
        self._output_view.push(val)

    def pull(self) -> Sequence[ValType]:
        return self._input_view.pull()

    @abstractmethod
    def run(self) -> None:
        pass


def main(stdscr):
    from optiface.cli import window

    window.init_curses(stdscr)
    header_win = window.HeaderWindow(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
