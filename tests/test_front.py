import pytest
from pathlib import Path
from front.app import OptiFaceTUI, OptiTop, SpaceView, MainCLI
from textual.widgets import Footer

from optiface.constants import (
    _PS_FILE,
    _EXPERIMENTS_DBFILE,
    _SPACE,
)

from optiface.cli import OptiFront, OptiWizard


# frontend component (i.e. first line command parser)
class TestOptiFront:
    _TEST_PSPACE_NAME: str = "testspace"

    def test_new(self):
        """
        Mock osm.add_new_pspace, assert that it is called when self.wizard.choice_input() in OptiFront.run() returns "new".
        """
        assert True

    def test_switch(self):
        assert True

    def test_exit(self):
        assert True


# textual TUI (on hold)
@pytest.fixture
def app():
    yield OptiFaceTUI()


@pytest.mark.asyncio
class TestApp:
    async def test_app_widget_initialization(self, app: OptiFaceTUI) -> None:
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.query_one(OptiTop) is not None
            assert app.query_one(SpaceView) is not None
            assert app.query_one(MainCLI) is not None
            assert app.query_one(Footer) is not None
