import importlib
import types

import pytest
from front.app import OptiFaceTUI, OptiTop, SpaceView, MainCLI
from textual.widgets import Footer


@pytest.fixture
def app():
    yield OptiFaceTUI()


@pytest.mark.asyncio
class TestSetup:
    async def test_front_import(self) -> None:
        module: types.ModuleType = importlib.import_module("front")
        assert module is not None


@pytest.mark.asyncio
class TestApp:
    async def test_app_widget_initialization(self, app: OptiFaceTUI) -> None:
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.query_one(OptiTop) is not None
            assert app.query_one(SpaceView) is not None
            assert app.query_one(MainCLI) is not None
            assert app.query_one(Footer) is not None
