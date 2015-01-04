"""ImportConfig base class spec."""
from __future__ import unicode_literals

import json
from unittest import TestCase

from importconfig import ImportConfig
from importconfig.importconfig import InvalidFilePathError


class TestSimpleImportConfig(TestCase):

    """Test the ImportConfig baseclass."""

    def setUp(self):
        """Create an instance of ImportConfig."""
        self.config = ImportConfig(json, './tests/resources/json/simple.json')

    def test_load_config(self):
        """Load the config into a dict, expanding any imports along the way.

        Asserting 'hello' is in the expanded result as "hello": "world" is
        in the imported file.
        """
        assert 'hello' in self.config.load().keys()

    def test__get_file_path(self):
        """Assert that ImportConfig#_get_file_path will load a file."""
        config = ImportConfig
        path = './tests/resources/json/simple.json'
        result = config._get_file_path(json, path)
        assert isinstance(result, dict)
        with self.assertRaises(InvalidFilePathError):
            config._get_file_path(json, 'not_a_file')

    def test_expand_basic(self):
        """Assert that the expand method will return a dict and check keys."""
        mock = {'foo': 'bar'}
        result = self.config._expand(mock)
        assert mock['foo'] == result['foo']

    def test_expand_import(self):
        """Assert that the expand method will import files."""
        mock = {'@file': './tests/resources/json/simple_import.json'}
        result = self.config._expand(mock)
        assert result['hello'] == 'world'


class TestImportConfigLazy(TestCase):

    """Test the laziness of the ImportConfig baseclass."""

    def test_importconfig_lazy(self):
        """Assert that the ImportConfig class will load a file lazily."""
        path = './tests/resources/json/simple.json'
        config = ImportConfig(json, path, lazy=True)
        assert config.object == {}
        assert config.config == {}
        result = config.load()
        assert config.object != {}
        assert config.config != {}
        assert bool(result)
