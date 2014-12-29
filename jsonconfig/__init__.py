"""ImportConfig

The special thing about Import is that it supports a notion
of "imports". You can import other json files in your json file
by specifying a "@file" value at any level in the config and it will
be expanded into that level.

A config file can be loaded lazily and the main config file will only be
loaded once it is called.

Example:

    {
        "app_name": "foo",
        "logging": {
            "@file": "logging.json",
            "level": "debug"
        }
    }

    will translate into:

    {
        "app_name": "foo",
        "logging": {
            "log_file": "/var/log/foo.log",
            "level": "debug"
        }
    }
"""

import collections
import os

import yaml

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json


__version__ = '0.0.1'
__author__ = 'Kasper M. Jacobsen'


class InvalidFilePathError(Exception):

    """Exception to be thrown when an invalid filepath is passed."""


class ImportConfig(object):

    """Base class for YamlConfig and JsonConfig."""

    def __init__(self, loader, file_path, lazy=False):
        """ImportConfig constructor."""
        self.loader = loader
        self.file_path = file_path
        self.object = {}
        self.config = {}
        if not lazy:
            self.object = self._get_file_path(self.loader, self.file_path)
            self.config = self._expand(self.object)

    @staticmethod
    def _get_file_path(loader, file_path):
        """Check the file path and return the JSON loaded as a dict.

        Arguments:
            file_path (``str``): Path to the file to load

        Returns:
            ``dict``
        """
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                return loader.load(f)
        raise InvalidFilePathError('{} is not a file!'.format(file_path))

    def _expand(self, d):
        """Iterate on the config object and find @file keys.

        Returns:
            ``dict``
        """
        result = {}
        for k, v in d.items():
            if k == '@file':
                result.update(self._get_file_path(self.loader, v))
            elif isinstance(v, collections.MutableMapping):
                # v and the result of _expand should be merged
                # with results' values taking precedence :*
                result[k] = self._expand(v)
            else:
                result[k] = v
        return result

    def load(self):
        """Loads up the expanded configuration.

        Returns:
            ``dict``
        """
        if not self.object:
            self.object = self._get_file_path(self.file_path)
            self.config = self._expand(self.object)
            return self.config
        return self.config


class JsonConfig(ImportConfig):

    """JsonConfig will load a JSON file into a dict.

    It can be used with UltraJSON, simplejson or the built in json module.

    Arguments:
        file_path (``str``): The path to the JSON file that will be loaded
        lazy (``bool``, optional): Do not load the JSON file immediately
            in the constructor. **default:** ``False``
    """

    def __init__(self, file_path, lazy=False):
        """JsonConfig constructor."""
        super(JsonConfig, self).__init__(json, file_path, lazy=lazy)


class YamlConfig(ImportConfig):

    """YamlConfig will load a yaml file into a dict.

    Arguments:
        file_path (``str``): The path to the yaml file that will be loaded
        lazy (``bool``, optional): Do not load the yaml file immediately
            in the constructor. **default:** ``False``
    """

    def __init__(self, file_path, lazy=False):
        """YamlConfig constructor."""
        super(YamlConfig, self).__init__(yaml, file_path, lazy=lazy)
