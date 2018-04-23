import os
import json

class JsonSettingsFile:
    '''
    Represents project info file in local director
    '''

    def __init__(self, path):
        self.__path = path
        self.__data = dict()

        if os.path.exists(self.__path):
            with open(self.__path, 'rb') as fh:
                self.__data = json.load(fh)


    def _save(self):
        with open(self.__path, 'wb') as fh:
            json.dump(self.__data, fh)


    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(JsonSettingsFile, self).__setattr__(key, value)
        else:
            self.__data[key] = value
            self._save()
    def __getattr(self, key):
        if key.startswith('_'):
            return super(JsonSettingsFile, self).__getattr__(key)
        else:
            try:
                return self.__data[key]
            except KeyError:
                return None

