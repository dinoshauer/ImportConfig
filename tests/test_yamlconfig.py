"""YamlConfig base class spec."""
from __future__ import unicode_literals

from unittest import TestCase

from importconfig import YamlConfig
from importconfig import yamlconfig


class TestYamlConfig(TestCase):

    """Test the YamlConfig class.

    This test doesn't need much as almost everything
    is covered in 'test_importconfig.py'.
    """

    def test_load_config(self):
        """Load the config into a dict, expanding any imports along the way.

        Asserting 'hello' is in the expanded result as "hello": "world" is
        in the imported file.
        """
        config = YamlConfig('./tests/resources/yaml/simple.yml')
        assert 'hello' in config.load().keys()

    def test_yamlconfig_method(self):
        """Test that the yamlconfig (method version) works.

        Asserting that jsonconfig will return a ``dict`` if ``lazy=False``
        or an instance of ``YamlConfig`` if ``lazy=True``.
        """
        eager = yamlconfig('./tests/resources/yaml/simple.yml', lazy=False)
        assert type(eager) is dict
        lazy = yamlconfig('./tests/resources/yaml/simple.yml', lazy=True)
        assert isinstance(lazy, YamlConfig)
