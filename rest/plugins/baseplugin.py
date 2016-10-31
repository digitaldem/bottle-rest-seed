# Standard Library imports
from __future__ import print_function
from inspect import getmro

# Package imports
from bottle import PluginError

# Local imports


class BasePlugin(object):
    api = 2

    def __init__(self, keyword=None, enforce_distinct=False):
        self.keyword = keyword
        self.enforce_distinct = enforce_distinct

    def setup(self, app):
        for plugin in app.plugins:
            if self.enforce_distinct and next((_ for _ in getmro(self.__class__) if _ != object and isinstance(type(plugin), _)), None):
                msg = 'Only one plugin of type [%s] can be used. Possibly enforce_distinct should be False.' % \
                      type(self)
                raise PluginError(msg)

            if self.keyword and self.keyword == plugin.keyword:
                msg = 'Plugin with keyword [%s] already in use. Attempted type [%s] conflicts with existing type [%s]' % \
                      (self.keyword, type(self), type(plugin))
                raise PluginError(msg)
