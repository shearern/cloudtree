import os
from hashlib import sha1

import sqlite3

class FileHashDB(object):
    '''Cache file content hashes'''

    CURRENT_DB_VERSION = 1

    def __init__(self, root_path, path):
        self.__root = root_path
        self.__path = path

        if os.path.exists(self.__path):
            self.db = sqlite3.connect(self.__path)
            if self.db_version != self.CURRENT_DB_VERSION:
                self.db = self.create_hash_cache_db(self.__path)
        else:
            self.db = self.create_hash_cache_db(self.__path)


    @staticmethod
    def create_hash_cache_db(path):

        if os.path.exists(path):
            os.unlink(path)

        db = sqlite3.connect(path)
        c = db.cursor()

        c.execute("""\
          CREATE TABLE version (
            version  integer)
          """)
        c.execute("""\
          CREATE TABLE hashes (
            name      text,
            size      integer,
            mtime     integer,
            sha1      text)
          """)
        c.execute("CREATE UNIQUE INDEX idx_hashes ON hashes (name)")

        c.execute("INSERT INTO version (version) VALUES (?)" % (FileHashDB.CURRENT_DB_VERSION))

        db.commit()

        return db


    def get_sha1(self, name, cache_only=False):
        '''Get hash for file or copmute if needed'''

        path = os.path.join(self.__path, name)

        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)

        # Get hash from db
        sql = """
          SELECT sha1
          FROM hashes
          WHERE name = ?
            AND size = ?
            AND mtime = ?
          """
        curs = self.db.cursor()
        for row in curs.execute(sql, (name, size, mtime)):
            return row[0]

        if cache_only:
            return None

        # Clear entry if needed
        sql = "DELETE FROM hashes WHERE path = ?"
        curs.execute(sql, (name, ))

        # Compute hash
        hasher = sha1()
        with open(path, 'rb') as fh:
            while True:
                data = fh.read(65536)
                if data:
                    hasher.update(data)
                else:
                    break
        file_hash = sha1.hexdigest()

        # Cache
        curs.execute("""
          INSERT INTO hashes (name, size , mtime, sha1)
          VALUES (?, ?, ?, ?) 
          """, (
            name,
            size,
            mtime,
            file_hash))
        self.db.commit()

        return file_hash

