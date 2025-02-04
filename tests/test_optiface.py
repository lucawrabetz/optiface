import importlib
import pytest
from typing import Any

from optiface.core.optispace import Feature


class TestSetup:
    def test_optiface_import(self):
        importlib.import_module("optiface")


class TestFeature:
    """
    Behaviors:
    - initializes a Feature as expected
    """

    DATA: dict[str, Any] = {
        "name": "set_name",
        "feature_type": str,
        "default": "test",
        "verbose_name": "Set Name",
        "short_name": "s_n",
    }

    STRING: str = (
        "feature: set_name, type: <class 'str'>, default: test, output names: 'Set Name', 's_n'"
    )

    def test_feature_init(self):
        set_name = Feature(**self.DATA)
        assert str(set_name) == self.STRING


class TestProblemSpace:
    """
    Behaviors:
    - read a problem space as expected
    """

    def test_ps_read(self):
        pass


class TestOptiSpace:
    """
    Behaviors:
    - switch between problem spaces as expected
    """

    def test_ps_switch(self):
        pass
