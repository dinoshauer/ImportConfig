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


class TestMasterPrecedence(TestCase):

    """Test the ImportConfig baseclass."""

    def test_master_precedence(self):
        """Assert that the master document will take presedence over loaded."""
        path = './tests/resources/json/master_precedence.json'
        config = ImportConfig(json, path)
        assert config.config['hello'] == 'testing'


class TestRelativeImportConfig(TestCase):

    """Test relative imports."""

    def test_relative_import(self):
        """Assert that ImportConfig can import files relative to the master."""
        path = './tests/resources/json/relative.json'
        self.config = ImportConfig(json, path)
        assert self.config.config.get('hello') == 'world'


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


class TestImportConfigComplex(TestCase):

    """Test that we can load a file and children in a complex manner."""

    def test_importconfig_complex(self):
        """Assert that the ImportConfig class will load all files."""
        mock = {
            u'file': {
                u'file': {
                    u'file': {
                        u'file': {
                            u'filename': u'level3.json'
                        },
                        u'filename': u'level2.json'
                    },
                    u'filename': u'level1.json'
                },
                u'filename': u'base.json'
            }
        }
        path = './tests/resources/json/complex/base.json'
        config = ImportConfig(json, path)
        assert mock == config.config
