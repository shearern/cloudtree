import os
from pathlib import Path
from textwrap import dedent

from .exceptions import WorkingFolderStructureError, WorkingFolderAlreadyExists
from .HashCache import FileHashDB
from .HostSettings import HostSettings
from .JsonSettingsFile import JsonSettingsFile

class WorkingFolder:
    '''
    Local copy of a repository

    Structure:
        .cloudtree/
            db/
                (hostguid).snapshots
                snapshots.db
            hashcache.db
            lockfile
            project.info
            tasks.db
            stage/...
        (files)
        .ctignore
    '''


    def __init__(self, path):
        self.__path = path
        if not os.path.exists(self.cloudtree_folder):
            raise WorkingFolderStructureError("Missing %s" % (self.cloudtree_folder))
        self.__hash_db = FileHashDB(os.path.join(self.cloudtree_folder, 'hashcache.db'))


    @property
    def path(self):
        return self.__path


    @property
    def cloudtree_folder(self):
        return os.path.join(self.path, '.cloudtree')


    def get_sha1(self, name):
        return self.__hash_db.get_sha1(name)


    @staticmethod
    def init_new_working_folder(path, url):
        '''
        Intialize folder structure new working folder

        :param path:
        :param url:
        :return: WorkingFolder
        '''
        path = Path(path)

        cloudtree_fold = path / '.cloudtree'
        if cloudtree_fold.exists():
            raise WorkingFolderAlreadyExists(
                "Working folder %s already exists" % (path))
        if not cloudtree_fold.exists():
            cloudtree_fold.mkdir()

        db_fold = cloudtree_fold / 'db'
        if not db_fold.exists():
            db_fold.mkdir()

        stage_fold = cloudtree_fold / 'stage'
        if not stage_fold.exists():
            stage_fold.mkdir()

        project_settings = JsonSettingsFile(str(cloudtree_fold / 'project.info'))
        project_settings.url = str(url)
        project_settings.state = None

        return WorkingFolder(path)


