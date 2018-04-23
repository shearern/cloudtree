

class CloudRepository:
    '''
    Represents cloud repository

    Structure:
        prefix/
            db/
                (hots guid).snapshots
            files/
                (sha1).(size).file
    '''

    def __init__(self, storage):
        self.storage = storage
