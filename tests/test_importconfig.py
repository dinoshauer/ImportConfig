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
        self.ic = ImportConfig(json, './tests/resources/json/simple.json')

    def test_load_config(self):
        """Load the config into a dict, expanding any imports along the way.

        Asserting 'hello' is in the expanded result as "hello": "world" is
        in the imported file.
        """
        assert 'hello' in self.ic.load().keys()

    def test__get_file_path(self):
        """Assert that ImportConfig#_get_file_path will load a file."""
        ic = ImportConfig
        result = ic._get_file_path(json, './tests/resources/json/simple.json')
        assert isinstance(result, dict)
        with self.assertRaises(InvalidFilePathError):
            ic._get_file_path(json, 'not_a_file')

    def test_expand_basic(self):
        """Assert that the expand method will return a dict and check keys."""
        mock = {'foo': 'bar'}
        result = self.ic._expand(mock)
        assert mock['foo'] == result['foo']

    def test_expand_import(self):
        """Assert that the expand method will import files."""
        mock = {'@file': './tests/resources/json/simple_import.json'}
        result = self.ic._expand(mock)
        assert result['hello'] == 'world'


class TestImportConfigLazy(TestCase):

    """Test the laziness of the ImportConfig baseclass."""

    def test_importconfig_lazy(self):
        """Assert that the ImportConfig class will load a file lazily."""
        ic = ImportConfig(json, './tests/resources/json/simple.json', lazy=True)
        assert ic.object == {}
        assert ic.config == {}
        result = ic.load()
        assert ic.object != {}
        assert ic.config != {}
        assert bool(result)
