import datetime
import re
import shutil
import warnings

from optiface.utils import _DATETIME_FORMAT

_TERMINAL_WIDTH: int = shutil.get_terminal_size((80, 20)).columns
_MARGIN: str = " " * 2
_SPECIAL_CHAR = "-"
_PRECISION = 2


def margin(indent: int = 1) -> str:
    return _MARGIN * indent


_OPTIFACE_UI_EMOJI = f"{margin(4)}:-] "


def opti_indent_string(time: bool = True) -> str:
    if time:
        return f"{_OPTIFACE_UI_EMOJI} [{datetime.datetime.now().strftime(_DATETIME_FORMAT)}] "
    return f"{_OPTIFACE_UI_EMOJI} "


def blank_opti_indent() -> str:
    return f"{_OPTIFACE_UI_EMOJI} {' ' * (len(opti_indent_string()) - (len(_OPTIFACE_UI_EMOJI) + 1))}"


# start of public "export" functions


def blank_line() -> None:
    print()


def separator_line() -> None:
    left_mg: str = margin(1)
    right_mg: str = margin(4)
    separator_line: str = (
        f"{left_mg}{_SPECIAL_CHAR * (_TERMINAL_WIDTH - len(left_mg) - len(right_mg))}{right_mg}"
    )
    print(separator_line)


def separator_block() -> None:
    separator_line()
    separator_line()


def format_numbers_in_string(s: str) -> str:
    if type(s) != str:
        warnings.warn(
            f"Expected string in format_numbers_in_string, got {type(s)}. Cannot guarantee proper formatting."
        )
        return s
    pattern: re.Pattern[str] = re.compile(r"(\d+\.\d+)")

    def repl(match):
        return f"{float(match.group()):.{_PRECISION}f}"

    return pattern.sub(repl, s)


def header(msg: str) -> None:
    """
    Parameter msg should be a single line.
    """
    blank_line()
    separator_block()
    msg = format_numbers_in_string(msg)
    print(f"{opti_indent_string(time=False)}{msg}")
    separator_block()
    blank_line()


def subheader(msg: str) -> None:
    """
    Parameter msg should be a single line.
    """
    msg = format_numbers_in_string(msg)
    blank_line()
    print(f"{opti_indent_string(time=False)}{msg}")
    blank_line()


def body(msg: str, special: bool = False) -> None:
    """
    Parameter msg can be multiline (include newline chars).
    """
    msgs: list[str] = msg.split("\n")
    full_indent_string: str = opti_indent_string()
    blank_indent_string: str = blank_opti_indent()
    first: bool = True
    for m in msgs:
        line: str = format_numbers_in_string(m)
        indent: str = blank_indent_string
        if first:
            indent = full_indent_string
            first = False
        if special:
            print(f"{indent}--> {line}! <--")
        else:
            print(f"{indent}-> {line}")


def main() -> None:
    message: str = "message"
    header(message)
    subheader(message)
    body(message)
    body(message, special=True)
    blank_line()
    separator_line()
    blank_line()
    separator_block()
    blank_line()


if __name__ == "__main__":
    main()
