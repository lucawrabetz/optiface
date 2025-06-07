import pytest
import types
import importlib


class TestSetup:
    def test_tui_import(self) -> None:
        module: types.ModuleType = importlib.import_module("front")
        assert module is not None

    def test_optiface_import(self):
        module = importlib.import_module("optiface")
        assert module is not None
