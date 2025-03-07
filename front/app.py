#!/usr/bin/env python3

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Static, Placeholder, Footer, Select, RichLog

from typing import Callable, Sequence, TypeVar, Generic

# CSS-CLI constants
_APP_GRID: str = "app_grid"
_OPTI_WIDGET: str = "opti_widget"
_LEFT_COL: str = "left_col"
_RIGHT_COL: str = "right_col"


class OptiTop(Placeholder):
    def __init__(self, content: str = "optitop"):
        super().__init__(label=content, classes=_OPTI_WIDGET)


class SpaceView(Placeholder):
    def __init__(self, content: str = "spaceview"):
        super().__init__(label=content, classes=_OPTI_WIDGET)


T = TypeVar("T")


class ValueSelected(Message, Generic[T]):
    def __init__(self, value: T) -> None:
        super().__init__()
        self.value: T = value


class AutoDestructSelect(Select[T], Generic[T]):
    async def on_select(self, event: Select.Changed) -> None:
        self.post_message(ValueSelected[T](event.value))
        self.remove()


class MainCLI(RichLog):
    current_handler: Callable[[ValueSelected], None] | None = None

    def ask_for_input(
        self,
        prompt: str,
        options: Sequence[tuple[str, T]],
        handler: Callable[[ValueSelected[T]], None],
    ) -> None:
        prompt_widget = Static(prompt)
        self.mount(prompt_widget)
        selector = AutoDestructSelect[T](options)
        self.mount(selector)
        self.app.set_focus(selector)
        self.current_handler = handler

    def on_mount(self) -> None:
        self.ask_for_input(
            "Select an option:",
            [("ERM", 1), ("PSM", 2), ("DMM", 3)],
            self.handle_selection,
        )

    @on(ValueSelected)
    def handle_input(self, message: ValueSelected) -> None:
        if self.current_handler:
            self.current_handler(message)
            self.current_handler = None

    def handle_selection(self, message: ValueSelected[int]) -> None:
        self.write(f"You selected: {message.value}")


class OptiFooter(Footer):
    def __init__(self):
        super().__init__(show_command_palette=False)
        self.set_reactive(Footer.compact, True)


class OptiFaceTUI(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Horizontal(id=_APP_GRID):
            with Vertical(id=_LEFT_COL):
                yield MainCLI()
            with Vertical(id=_RIGHT_COL):
                yield OptiTop()
                yield SpaceView()
        yield OptiFooter()


if __name__ == "__main__":
    app = OptiFaceTUI()
    app.run()
