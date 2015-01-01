"""ImportConfig

The special thing about ImportConfig is that it supports a notion
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
from __future__ import unicode_literals

from importconfig import ImportConfig
from jsonconfig import JsonConfig
from yamlconfig import YamlConfig

__all__ = ('ImportConfig', 'JsonConfig', 'YamlConfig', )
__name__ = 'ImportConfig'
__url__ = 'https://github.com/Dinoshauer/ImportConfig'
__author__ = 'Kasper M. Jacobsen'
__email__ = 'k@mackwerk.dk'
__version__ = '0.0.1'