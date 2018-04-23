
class UsageError(Exception):
    def __init__(self, error, cmd=None):
        self.cmd = cmd
        super(UsageError, self).__init__(error)

class InvalidUrl(NotImplementedError): pass
class WorkingFolderStructureError(Exception): pass
class WorkingFolderAlreadyExists(Exception): pass
