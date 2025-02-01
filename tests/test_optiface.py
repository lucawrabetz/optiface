import pytest
import importlib


class TestSetup:
    def test_optiface_import(self):
        importlib.import_module("optiface")
