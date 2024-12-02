import curses
import time

from optiface.service import api
from optiface.cli import window


class ExampleService(api.ServiceAdaptor[str]):
    def __init__(
        self,
        input_view: window.ServiceWindow,
        output_view: window.ServiceWindow,
    ):
        super().__init__(input_view, output_view)

    def run(self) -> None:
        i: int = 1
        while True:
            self._output_view.push(f"iteration: {i}")
            i += 1
            time.sleep(0.2)


def main(stdscr):
    cli = window.opti_cli_init(stdscr)
    exs = ExampleService(cli.service, cli.service)
    exs.run()


if __name__ == "__main__":
    curses.wrapper(main)
