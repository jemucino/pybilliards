# -*- coding: utf-8 -*-

import logging
import os

# TODO: replace platform specific paths

class Settings(object):
    def __init__(self):
        self._settings = {}
        #self.userdir = self._settings['userdir'] = os.path.join(os.path.expanduser('~'),'.config','pybilliards')
        self.add_from_file(os.path.join('settings_default.py'))
        self.userdir = self._settings['userdir']
        self.add_from_file(os.path.join(self.userdir,'user_settings.py'))

    def get(self, key):
        keys = key.split('.')
        value = self._settings
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            logging.info('No setting found for key: %s'%key)
            value = None
        return value

    def set(self, key, value):
        keys = key.split('.')
        v = self._settings
        for k in keys[:-1]:
            try:
                v = v[k]
            except KeyError:
                v[k] = {}
                v = v[k]
        v[keys[-1]] = value

    def add_from_file(self, filename):
        d = {}
        try:
            execfile(filename, d)
            data = d['settings']
            self._settings.update(data)
        except Exception, exc:
            logging.warn(repr(exc))
            logging.warn('Unable top load settings from: %s'%filename)

settings = Settings()
