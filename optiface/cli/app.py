from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Placeholder, Footer, Static

# CSS-CLI constants
_APP_GRID: str = "app_grid"
_OPTI_WIDGET: str = "opti_widget"
_RIGHT_COL: str = "right_col"
_MAIN_CLI: str = "main_cli"


class OptiTop(Placeholder):
    def __init__(self, content: str = "optitop"):
        super().__init__(label=content, classes=_OPTI_WIDGET)


class SpaceView(Placeholder):
    def __init__(self, content: str = "spaceview"):
        super().__init__(label=content, classes=_OPTI_WIDGET)


class MainCLI(Placeholder):
    def __init__(self):
        super().__init__("main-cli", classes=_OPTI_WIDGET, id=_MAIN_CLI)


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
            yield MainCLI()
            with Vertical(id=_RIGHT_COL):
                yield OptiTop()
                yield SpaceView()
        yield OptiFooter()


if __name__ == "__main__":
    app = OptiFaceTUI()
    app.run()
