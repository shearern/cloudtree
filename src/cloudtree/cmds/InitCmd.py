import os

from ..core.exceptions import UsageError, InvalidUrl
from ..core.CloudURL import CloudURL
from .CTCommand import CTCommand, CTCommandArgs

class InitCmd(CTCommand):
    '''
    Command to initialize cloud folder for source control
    '''

    name = 'init'

    usage = '''\
        init path
        
        path:
            Path to cloud directory to create repository in
            example: b2://bucket_name/prefix
        '''

    def parse_args(self, argv):

        # Init
        args = CTCommandArgs()
        args.path = None

        # Parse
        for arg in self._read_arguments(argv):
            if arg.type == 'posarg' and arg.pos == 0:
                try:
                    args.path = CloudURL(arg.value)
                except InvalidUrl as e:
                    raise UsageError(str(e))
            else:
                raise UsageError(cmd=self, error="Unknown argument: " + str(arg))

        # Validate
        if args.path is None:
            raise UsageError("Cloud path is required")

        return args

    def execute(self, argv):

        args = self.parse_args(argv)

        print("Initalizing " + str(args.path))

        # Check exists

        # Create