
from .SnapshotsFile import SnapshotsFile


def initialize_repository(url):

    # Initialize first snapshot
    snapshots =  SnapshotsFile.init_new()