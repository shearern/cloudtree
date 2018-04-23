from usersettings import Settings
from socket import gethostname
from random import random

class HostSettings:

    def __init__(self):
        self.__settings = Settings('net.shearern.cloudtree')

        self.__settings.add_setting('hostname', str)
        self.__settings.add_setting('host_id', str)
        self.__settings.load_settings()

        if self.hostname is None:
            self.hostname = gethostname()
        if self.host_id is None:
            self.host_id = '%020x' % (random.getrandbits(20*8))


    @property
    def hostname(self):
        return self.__settings.hostname
    @hostname.setter
    def set_hostname(self, value):
        self.__settings.hostname = value
        self.__settings.save_settings()

    @property
    def host_id(self):
        return self.__settings.host_id
    @host_id.setter
    def set_hostname(self, value):
        self.__settings.host_id = value
        self.__settings.save_settings()
