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


def main(stdscr):
    from optiface.cli import window

    window.init_curses(stdscr)
    header_win = window.HeaderWindow(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
