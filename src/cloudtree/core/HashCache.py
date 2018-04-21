import os
from threading import RLock

from tinydb import TinyDB, Query

from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDesktopServices

from ..core import define_setting, SbcCatalogSettings


def default_hash_db_path():
        app_dir_folder = QDesktopServices.storageLocation(QDesktopServices.DataLocation)
        try:
            if not os.path.exists(app_dir_folder):
                os.makedirs(app_dir_folder)
        except Exception, e:
            print "Failed to calc path to save file hashes: " + str(e)

        return os.path.join(app_dir_folder, 'file_hash.json')


define_setting('file_hash_db/path', default_hash_db_path())


class FileHashDB(object):
    '''Cache file content hashes'''

    def __init__(self):
        self._lock = RLock()
        self.settings = SbcCatalogSettings()
        self._db = TinyDB(self.cache_path())


    def cache_path(self):
        return self.settings.get('file_hash_db/path')


    def get(self, path, size, mtime):
        with self._lock:
            Hash = Query()
            for doc in self._db.search(Hash.path == path):
                try:
                    if doc['mtime'] == mtime:
                        if doc['size'] == size:
                            return doc['hash']
                except KeyError:
                    pass


    def add(self, path, size, mtime, hash):
        Hash = Query()
        self._db.remove(Hash.path == path)
        self._db.insert({
            'path':     path,
            'size':     size,
            'mtime':    mtime,
            'hash':     hash,
        })
