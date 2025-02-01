import pytest
import importlib


class TestSetup:
    def test_front_import(self):
        importlib.import_module("front")
