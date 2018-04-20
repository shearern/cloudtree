import re

from ..core.exceptions import InvalidUrl

class CloudURL:
    '''URL to a cloud service'''

    PAT = re.compile(r'^([^\/]+):\/\/([^\/]+)(\/(.*))?$')

    def __init__(self, url):
        self.__url = url
        self.__parsed = self.PAT.match(url)

        # Validate
        if self.cloud_service not in ('b2', ):
            raise InvalidUrl("URL %s invalid.  Cloud Service %s is not supported" % (self.url, self.cloud_service))
        if self.bucket is None or len(self.bucket) == 0:
            raise InvalidUrl("URL %s invalid.  Bucket is required." % (self.url))


    @property
    def url(self):
        return self.__url

    @property
    def cloud_service(self):
        return self.__parsed.group(1)

    @property
    def bucket(self):
        return self.__parsed.group(2)

    @property
    def prefix(self):
        return self.__parsed.group(3) or None



    def __str__(self):
        return self.__url
    def __repr__(self):
        return "CloudURL(%s)" % (repr(self.__url))