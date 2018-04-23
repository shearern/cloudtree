import os

from ..core.exceptions import UsageError, InvalidUrl
from ..core.CloudURL import CloudURL
from ..core.WorkingFolder import WorkingFolder

from .CTCommand import CTCommand, CTCommandArgs

class InitCmd(CTCommand):
    '''
    Command to join local folder to cloud repository, creating if necessary
    '''

    name = 'init'

    usage = '''\
        init cloud_path local_path
        
        cloud_path:
            Path to cloud directory to create repository in
            example: b2://bucket_name/prefix
            
        local_path:
            Path to local folder to pair with
        '''

    def parse_args(self, argv):

        # Init
        args = CTCommandArgs()
        args.path = None

        # Parse
        for arg in self._read_arguments(argv):
            if arg.type == 'posarg' and arg.pos == 0:
                try:
                    args.cloud_path = CloudURL(arg.value)
                except InvalidUrl as e:
                    raise UsageError(str(e))
            if arg.type == 'posarg' and arg.pos == 1:
                args.local_path = arg.value
            else:
                raise UsageError(cmd=self, error="Unknown argument: " + str(arg))

        # Validate
        if args.cloud_path is None:
            raise UsageError("Cloud path is required")
        if args.local_path is None:
            raise UsageError("Local path is required")
        args.local_path_parent = os.path.abspath(os.path.dirname(args.local_path))
        if not os.path.exists(args.local_path_parent):
            raise UsageError("Parent path %s doesn't exist" % (args.local_path_parent))

        return args

    def execute(self, argv):

        args = self.parse_args(argv)

        if not os.path.exists(args.local_path):
            os.path.mkdir(args.local_path)
        local = WorkingFolder.init_new_working_folder(args.local_path)

