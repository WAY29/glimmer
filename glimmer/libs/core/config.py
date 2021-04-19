from configparser import ConfigParser

"""
CONFIG
    base:
    - root_path ""
    - targets []
    - request {}
    - config ConfigHandler
    option:
    - verbose 0
    - very_verbose 0

PLUGINS
    debug_messages ""
    messages ""
    instances {}
    type:
        module

POCS
    debug_messages ""
    messages ""
    modules {}
    type:
        module

"""

from collections import OrderedDict


class AttribDict(OrderedDict):
    """
    AttrDict extends OrderedDict to provide attribute-style access.
    Items starting with __ or _OrderedDict__ can't be accessed as attributes.

    Reference: https://github.com/knownsec/pocsuite3/
    """
    __exclude_keys__ = set()

    def __getattr__(self, name):
        if (name.startswith('__')
                or name.startswith('_OrderedDict__')
                or name in self.__exclude_keys__):
            return super(AttribDict, self).__getattribute__(name)
        else:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name, value):
        if (name.startswith('__')
                or name.startswith('_OrderedDict__')
                or name in self.__exclude_keys__):
            return super(AttribDict, self).__setattr__(name, value)
        self[name] = value

    def __delattr__(self, name):
        if (name.startswith('__')
                or name.startswith('_OrderedDict__')
                or name in self.__exclude_keys__):
            return super(AttribDict, self).__delattr__(name)
        del self[name]


class ConfigHandler:
    def __init__(self, config_path=""):
        self._config = ConfigParser()
        self.config_path = config_path
        if config_path:
            self._config.read(config_path)

    def loads(self, config_path):
        self._config.load(config_path)

    def sections(self):
        if not hasattr(self, "_sections"):
            self._sections = self._config.sections()
        return self._sections

    def get(self, search_key, default=""):
        all_keys = self.sections()
        len_of_search_key = len(search_key)
        if search_key in all_keys:
            return self._config[search_key]
        else:
            results = {}
            for k in all_keys:
                if k.startswith(search_key):
                    results[k[len_of_search_key+1:]] = dict(self._config[k])
            if results:
                return results
        return default


CONFIG = AttribDict()
CONFIG.base = AttribDict()
CONFIG.option = AttribDict()

POCS = AttribDict()
POCS.modules = AttribDict()

PLUGINS = AttribDict()
PLUGINS.instances = AttribDict()
