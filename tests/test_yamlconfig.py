"""YamlConfig base class spec."""
from __future__ import unicode_literals

from unittest import TestCase

from importconfig import YamlConfig


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
