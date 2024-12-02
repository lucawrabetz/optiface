"""
throughout, size, height, width are in the following units:
  - horizontal: number of characters
  - vertical: number of lines
  - stdscr: parent window
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import curses
from dataclasses import dataclass
import datetime
from enum import Enum
import random
import re
from typing import final
from typing import TypeAlias

from optiface.service import api
from optiface.cli import pick

# constants
_DATE_FORMAT = "%B %d, %Y"
_TIME_FORMAT = "%H:%M:%S %p"
_SPECIAL_CHAR = "="
_COPYRIGHT_CHAR = chr(169)
_OPTIFACE_UI_EMOJI = ":-]"
_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

_SINGLE_HINDENT_SCREEN_DIVIDER = 150
_MIN_HINDENT_SIZE = 1
_SINGLE_VINDENT_SCREEN_DIVIDER = 100
_MIN_VINDENT_SIZE = 0
_DEFAULT_SMALL_INDENT = 1
_DEFAULT_MEDIUM_INDENT = 2
_DEFAULT_LARGE_INDENT = 5
_PRECISION = 2


# useful lightweight structs for size stuff
@dataclass(frozen=True)
class WindowDim:
    y: int
    x: int
    height: int
    width: int

    @classmethod
    def from_window(cls, win):
        height, width = win.getmaxyx()
        y, x = win.getbegyx()
        return cls(y=y, x=x, height=height, width=width)


def hindent_size(dim: WindowDim) -> int:
    # number of characters for a single horizontal indent
    return max(_MIN_HINDENT_SIZE, int(dim.width / _SINGLE_HINDENT_SCREEN_DIVIDER))


def vindent_size(dim: WindowDim) -> int:
    # number of characters for a single vertical indent
    return max(_MIN_VINDENT_SIZE, int(dim.height / _SINGLE_VINDENT_SCREEN_DIVIDER))


@dataclass(frozen=True)
class MarginDim:
    """
    indent: number of indents in pre and post
      - f"{pre}{text}{post}" for horizontal
      - pre, lines, post for for vertical
      pre and post being spaces or empty lines
    """

    indent: int
    pre: int
    text: int
    post: int

    @classmethod
    def hcentered(cls, dim: WindowDim, indent: int) -> MarginDim:
        indent_size = hindent_size(dim) * indent
        return cls(
            indent=indent,
            pre=indent_size,
            text=dim.width - indent_size,
            post=indent_size,
        )

    @classmethod
    def vcentered(cls, dim: WindowDim, indent: int) -> MarginDim:
        indent_size = vindent_size(dim) * indent
        return cls(
            indent=indent,
            pre=indent_size,
            text=dim.height - indent_size,
            post=indent_size,
        )


def hcenter_margin(dim: WindowDim, indent: int) -> str:
    margin = " " * MarginDim.hcentered(dim, indent).pre
    return margin


# string utilities and wrappers
def format_numbers_in_string(s: str) -> str:
    if type(s) != str:
        return s
    pattern: re.Pattern[str] = re.compile(r"(\d+\.\d+)")

    def repl(match):
        return f"{float(match.group()):.{_PRECISION}f}"

    return pattern.sub(repl, s)


def fill_with_spaces(window_dim: WindowDim, s: str) -> str:
    return s + " " * (window_dim.width - len(s))


def format_now(dt_format) -> str:
    return datetime.datetime.now().strftime(dt_format)


def opti_indent_string(
    window_dim: WindowDim, time: bool = False, indent: int = _DEFAULT_LARGE_INDENT
) -> str:
    margin = hcenter_margin(window_dim, indent)
    emoji_indent = f"{margin}{_OPTIFACE_UI_EMOJI} "
    if time:
        return f"{emoji_indent} [{format_now(_TIME_FORMAT)}] "
    return emoji_indent


def blank_opti_indent(
    window_dim: WindowDim, indent: int = _DEFAULT_LARGE_INDENT
) -> str:
    margin = hcenter_margin(window_dim, indent)
    emoji_indent = f"{margin}{_OPTIFACE_UI_EMOJI} "
    return f"{emoji_indent} {' ' * (len(opti_indent_string(window_dim, time=False, indent=indent)) - (len(emoji_indent) + 1))}"


def separator_line(
    window_dim: WindowDim, indent: int = _DEFAULT_SMALL_INDENT, border: bool = False
) -> str:
    margin: str = hcenter_margin(window_dim, indent)
    width = window_dim.width
    if border:
        width -= 4
    separator_line: str = f"{margin}{_SPECIAL_CHAR * (width - 2 * len(margin))}{margin}"
    return separator_line


def blank_line(window_dim: WindowDim, border: bool = False) -> str:
    width: int = window_dim.width
    if border:
        width -= 2
    return " " * width


def footer_string(window_dim: WindowDim) -> str:
    return fill_with_spaces(
        window_dim,
        f"{opti_indent_string(window_dim, False)} {_COPYRIGHT_CHAR} opti-face",
    )


def header_string(window_dim: WindowDim) -> str:
    return fill_with_spaces(
        window_dim,
        f"{opti_indent_string(window_dim, False)} opti-face - {format_now(_DATE_FORMAT)}",
    )


def header_buffer(window_dim: WindowDim, indent: int = _DEFAULT_SMALL_INDENT) -> str:
    sep = separator_line(window_dim, indent)
    blank = blank_line(window_dim)
    head: str = f"{sep}{header_string(window_dim)}{blank}{sep}"
    return head


def footer_buffer(window_dim: WindowDim, indent: int = _DEFAULT_SMALL_INDENT) -> str:
    sep = separator_line(window_dim, indent)
    footer: str = f"{sep}{footer_string(window_dim)}"
    return footer


# dimension factories
def string_height(window_dim: WindowDim, s: str) -> int:
    """
    returns the number of lines in a string as currently formatted, returning 0 if the string is empty
    """
    if len(s) == 0:
        return 0
    return max(1, int(len(s) / window_dim.width))


def window_dim(win, off_dim: WindowDim | None = None) -> WindowDim:
    parent_dim = WindowDim.from_window(win)
    if off_dim:
        return WindowDim(
            parent_dim.y + off_dim.y,
            parent_dim.x + off_dim.x,
            off_dim.height,
            off_dim.width,
        )
    return WindowDim(
        parent_dim.y,
        parent_dim.x,
        parent_dim.height,
        parent_dim.width,
    )


def header_dim(win) -> WindowDim:
    parent_dim = WindowDim.from_window(win)
    off_dim = WindowDim(
        parent_dim.y,
        parent_dim.x,
        string_height(parent_dim, header_buffer(parent_dim)) + 1,
        int(parent_dim.width / 3),
    )
    return window_dim(win, off_dim)


def footer_dim(win) -> WindowDim:
    parent_dim = WindowDim.from_window(win)
    height = string_height(parent_dim, footer_buffer(parent_dim)) + 1
    off_dim = WindowDim(
        parent_dim.y + parent_dim.height - height,
        parent_dim.x,
        height,
        parent_dim.width,
    )
    return window_dim(win, off_dim)


# color definitions
class Color(Enum):
    DEFAULT = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    MAGENTA = 5
    ORANGE = 6


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(Color.RED.value, curses.COLOR_RED, -1)
    curses.init_pair(Color.GREEN.value, curses.COLOR_GREEN, -1)
    curses.init_pair(Color.BLUE.value, curses.COLOR_BLUE, -1)
    curses.init_pair(Color.YELLOW.value, curses.COLOR_YELLOW, -1)
    curses.init_pair(Color.MAGENTA.value, curses.COLOR_MAGENTA, -1)
    curses.init_color(6, 1000, 500, 0)  # RGB (1000, 500, 0) -> Orange-brown
    curses.init_pair(Color.ORANGE.value, 6, -1)


@dataclass(frozen=True)
class WinColorConfig:
    body = Color.DEFAULT
    special = Color.ORANGE
    good = Color.GREEN
    bad = Color.RED


Window: TypeAlias = curses.window


class BaseWindow(api.IOView[str]):
    def __init__(self, stdscr, border: bool):
        self._scroll: bool = self.scroll_from_parent()
        self._border: bool = border
        self._parent = stdscr
        self._dim: WindowDim = self.dim_from_parent()
        self._win: Window = curses.newwin(
            self._dim.height, self._dim.width, self._dim.y, self._dim.x
        )
        self._colors: WinColorConfig = self.colors_from_parent()
        self._win.scrollok(self._scroll)
        self._win.clear()
        self._zero: int = 0
        if border:
            self._win.box()
            self._zero = 1
            self._win.move(self._zero, self._zero)
        self._win.refresh()

    @property
    def y(self) -> int:
        return self._dim.y

    @property
    def x(self) -> int:
        return self._dim.x

    @property
    def height(self) -> int:
        return self._dim.height

    @property
    def width(self) -> int:
        return self._dim.width

    @property
    def curs(self) -> tuple[int, int]:
        return self._win.getyx()

    # input
    def get_char_input(self) -> int:
        return self._win.getch()

    def get_single_choice(self, *options: str, title="select an option:"):
        choice = pick.pick(options=options, title=title, screen=self._win)[0]
        self.new_line()
        return choice

    # printing utilities
    def new_line(self) -> None:
        y, _ = self._win.getyx()
        if y == self._dim.height - 1:
            # TODO: edge case here, scroll will return error if scroll is not enabled
            self._win.scroll(1)
            self._win.move(y, self._zero)
        else:
            self._win.move(y + 1, self._zero)
        self._win.refresh()

    def print_buf(self, s: str, color: Color | None, new_line: bool) -> None:
        y, x = self._win.getyx()
        if x == 0 and self._zero == 1:
            self._win.move(y, self._zero)
        # more than a line wraps
        if color is not None:
            self._win.attron(curses.color_pair(color.value))
        self._win.addstr(s)
        if color is not None:
            self._win.attroff(curses.color_pair(color.value))
        if not new_line:
            self._win.refresh()
            return
        y, x = self._win.getyx()
        if x == self._zero:
            self._win.refresh()
            return
        self.new_line()

    def separator_line(self, color: Color | None = None) -> None:
        s: str = separator_line(self._dim, border=self._border)
        self.print_buf(s, color, False)

    # runtime initialization
    def dim_from_parent(self) -> WindowDim:
        return WindowDim(0, 0, self._parent.height, self._parent.width)

    def scroll_from_parent(self) -> bool:
        return False

    def colors_from_parent(self) -> WinColorConfig:
        return WinColorConfig()

    # runtime print strings
    def body_string(self, l: str) -> str:
        return opti_indent_string(self._dim) + l

    def emptybody_string(self, l: str) -> str:
        return hcenter_margin(self._dim, _DEFAULT_MEDIUM_INDENT) + l

    def special_string(self, l: str) -> str:
        return opti_indent_string(self._dim, time=True) + l

    # public interface for printing messages
    def body(self, l: str, color: Color | None = None) -> None:
        s: str = self.body_string(l)
        self.print_buf(s, color, True)

    def emptybody(
        self, l: str, color: Color | None = None, new_line: bool = True
    ) -> None:
        s: str = self.emptybody_string(l)
        self.print_buf(s, color, new_line)

    @final
    def special(self, l: str, sep: bool = True) -> None:
        self.new_line()
        if sep:
            self.separator_line(self._colors.special)
            self.new_line()  # to end separator line
        self.print_buf(self.special_string(l), self._colors.special, new_line=True)

    def print_bufs(
        self, *bufs: tuple[str, Color | None], new_line: bool = True
    ) -> None:
        for text, color in bufs:
            self.print_buf(text, color, new_line)

    def remove(self) -> curses.window:
        self._win.clear()
        self._win.refresh()
        self._parent.touchwin()
        self._parent.refresh()

        del self._win
        return self._parent

    # optiio interface
    def push(self, val: str, special: bool = False) -> None:
        if special:
            self.special(val)
        else:
            self.body(val)
        self.new_line()

    def pull(self) -> list[str]:
        return [chr(self.get_char_input())]


# fixed windows
class HeaderWindow(BaseWindow):
    def __init__(self, stdscr, border: bool = False):
        super().__init__(stdscr, border)
        self._header: str = header_buffer(self._dim)
        self.fill()

    def dim_from_parent(self) -> WindowDim:
        return header_dim(self._parent)

    def fill(self):
        self.print_buf(self._header, None, new_line=False)

    def scroll_from_parent(self) -> bool:
        return False

    def emptybody_string(self, l: str) -> str:
        return l

    def body_string(self, l: str) -> str:
        return l


class FooterWindow(BaseWindow):
    def __init__(self, stdscr, border: bool = False):
        super().__init__(stdscr, border)
        self._footer: str = footer_buffer(self._dim)
        self.fill()

    def dim_from_parent(self) -> WindowDim:
        return footer_dim(self._parent)

    def fill(self):
        self.print_buf(self._footer, color=None, new_line=False)

    def scroll_from_parent(self) -> bool:
        return False

    def emptybody_string(self, l: str) -> str:
        return l

    def body_string(self, l: str) -> str:
        return l


# interactive windows
class UIWindow(BaseWindow):
    def __init__(self, stdscr, off_dim: WindowDim | None = None, border: bool = False):
        self._off_dim = off_dim
        super().__init__(stdscr, border)

    def dim_from_parent(self) -> WindowDim:
        return window_dim(self._parent, self._off_dim)

    def scroll_from_parent(self) -> bool:
        return True


class ServiceWindow(BaseWindow):
    def __init__(self, stdscr, off_dim: WindowDim | None = None, border: bool = False):
        self._off_dim = off_dim
        super().__init__(stdscr, border)

    def emptybody_string(self, l: str) -> str:
        return hcenter_margin(self._dim, _DEFAULT_SMALL_INDENT) + l

    def body_string(self, l: str) -> str:
        return hcenter_margin(self._dim, _DEFAULT_MEDIUM_INDENT) + l

    def dim_from_parent(self) -> WindowDim:
        return window_dim(self._parent, self._off_dim)

    def scroll_from_parent(self) -> bool:
        return True


_CONTINUE = "(*)ontinue:"
_QUIT_OR_ANY = "(q)uit or (*):"


def testpause_rep(
    main_win, prompt: str = _QUIT_OR_ANY, color: Color = Color.YELLOW
) -> int:
    main_win.push(prompt)
    key: int = main_win.get_char_input()
    if chr(key) == "q":
        # TODO - the interface for the UI should probably have a convenient
        # quitting mechanism
        main_win.body(f"QUIT")
    main_win.body(f"You pressed {key}! {_CONTINUE}", color=color)
    quit = main_win.get_char_input()
    return quit


def testchoice_rep(
    main_win, prompt: str = "select a character:", color: Color = Color.MAGENTA
) -> str:
    chars = random.sample(_ALPHABET, k=9)
    choice = main_win.get_single_choice(*chars, title=prompt)
    main_win.new_line()
    main_win.push(f"You chose {choice[0]}! {_CONTINUE}")
    _ = main_win.get_char_input()
    main_win.new_line()
    return choice[0]


def init_curses(stdscr):
    curses.curs_set(0)
    init_colors()
    curses.use_default_colors()
    stdscr.bkgd(" ", curses.color_pair(0))


@dataclass
class CLI:
    header: HeaderWindow
    footer: FooterWindow
    status: UIWindow
    main: UIWindow
    service: ServiceWindow


def opti_cli_init(stdscr) -> CLI:
    init_curses(stdscr)
    header_win = HeaderWindow(stdscr)
    footer_win = FooterWindow(stdscr)
    y, x = stdscr.getmaxyx()
    main_height: int = y - header_win.height - footer_win.height
    main_off_dim = WindowDim(
        y=header_win.height, x=0, height=main_height, width=header_win.width
    )
    status_width: int = x - header_win.width
    status_off_dim = WindowDim(
        y=0, x=header_win.width, height=header_win.height, width=status_width
    )
    main_win = UIWindow(stdscr, main_off_dim)
    status_win = UIWindow(stdscr, status_off_dim)

    status_win.separator_line(color=Color.GREEN)
    status_win.emptybody("problemspace: PASSING solver: PASSING", Color.GREEN)
    status_win.emptybody("some kind of database STATUS")
    status_win.separator_line(color=Color.GREEN)
    service_off_dim = WindowDim(
        y=main_off_dim.y,
        x=status_off_dim.x,
        height=main_off_dim.height,
        width=status_off_dim.width,
    )
    service_win = ServiceWindow(stdscr, service_off_dim)
    return CLI(
        header=header_win,
        footer=footer_win,
        service=service_win,
        main=main_win,
        status=status_win,
    )


def main(stdscr):
    cli = opti_cli_init(stdscr)
    i: int = 1
    service_y, _ = cli.service.curs
    while service_y != cli.service.height - 1:
        key: int = 0
        if i % 10 == 0:
            cli.main.push("multiple of 10!", special=True)
            cli.service.push("multiple of 10!", special=True)
        elif i % 4 == 0:
            service_y, _ = cli.service.curs
            key = testpause_rep(
                cli.service, "welcome to this window! (q) or (*)", Color.MAGENTA
            )
        else:
            key = testpause_rep(cli.main)
            if chr(key) == "q":
                break
            s: str = testchoice_rep(cli.service)
        i += 1
        service_y, _ = cli.service.curs


if __name__ == "__main__":
    curses.wrapper(main)
