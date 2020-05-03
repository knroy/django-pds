"""
Settings and configuration for django_pds.

this file is re-created from django.conf.__init__.py file
main reason of this settings to lazy load all the configuration
from either django_pds.core.settings file or to load
settings for django_pds defined in django project settings
"""

import importlib

from django.utils.functional import LazyObject, empty
from mongoengine import ImproperlyConfigured

from .core.utils import get_environment

ENVIRONMENT_VARIABLE = "DJANGO_PDS_SETTINGS_MODULE"

DEFAULT_CORE_SETTINGS_MODULE = 'django_pds.core.settings'

list_settings = [
    "SYSTEM_SUPPORTED_ROLES",
    "SECURITY_ATTRIBUTES",
    "SECURITY_ROLES_ATTRIBUTES",
    "SECURITY_IDS_ATTRIBUTES",
    "READ_ONLY_FIELDS",
    "SELECT_NOT_ALLOWED_ENTITIES",
    "READ_NOT_ALLOWED_ATTRIBUTES",
    "MONGO_ENGINE_USABLE_OPERATORS",
    "EDIT_NOT_ALLOWED_ATTRIBUTES_PDS"
]


class LazySettings(LazyObject):

    def _setup(self, name=None):

        default_settings_module = DEFAULT_CORE_SETTINGS_MODULE
        self._wrapped = Settings(default_settings_module)

        override_settings_module = get_environment(ENVIRONMENT_VARIABLE, False, None)
        print(override_settings_module)
        if override_settings_module:
            override_settings = SettingsOverride(self._wrapped)
            override_settings.override(override_settings_module)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<django_pds.conf.LazySettings [Unevaluated]>'
        return '<django_pds.conf.LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self.__dict__."""
        if self._wrapped is empty:
            self._setup(name)
        val = getattr(self._wrapped, name)
        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        """
        Set the value of setting. Clear all cached values if _wrapped changes
        (@override_settings does this) or clear single values when set.
        """
        if name == '_wrapped':
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete a setting and clear it from cache if needed."""
        super().__delattr__(name)
        self.__dict__.pop(name, None)


class Settings:
    def __init__(self, settings_module):
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in list_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)


class SettingsOverride:

    def __init__(self, __settings):
        self.__settings = __settings

    def override(self, override_module):

        mod = importlib.import_module(override_module)

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in list_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self.__settings, setting, setting_value)


settings = LazySettings()
