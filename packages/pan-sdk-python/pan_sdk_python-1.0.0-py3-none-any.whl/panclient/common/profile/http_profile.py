class HttpProfile(object):
    def __init__(self, protocol=None, endpoint=None, reqMethod="POST", reqTimeout=60,
                 keepAlive=False):
        """HTTP profile.
        :param protocol: temporarily useless,set None
        :type protocol: str
        :param endpoint: The domain to access, like: cvm.tencentcloudapi.com
        :type endpoint: str
        :param reqMethod: the http method, valid choice: GET, POST
        :type reqMethod: str
        :param reqTimeout: The http timeout in second.
        :type reqTimeout: int
        """
        self.endpoint = endpoint
        self.reqTimeout = 60 if reqTimeout is None else reqTimeout
        self.reqMethod = "POST" if reqMethod is None else reqMethod
        self.protocol = protocol
        self.keepAlive = keepAlive

