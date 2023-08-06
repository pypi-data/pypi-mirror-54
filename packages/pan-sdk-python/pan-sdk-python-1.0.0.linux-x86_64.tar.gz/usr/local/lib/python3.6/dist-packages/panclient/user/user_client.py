import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie


class UserClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''

    def get_user_me(self):
        try:
            self._requestPath = "/panorama/user/me"
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            params = ""
            c = cookie.Cookie()
            print(c.get_cookie())
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def get_all_user(self, request):
        try:
            self._requestPath = "/panorama/user/all"
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request._serialize()
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def add_user(self, request):
        try:
            self._requestPath = "/panorama/v2/user"
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request._serialize()
            print("params", params)
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def mod_user(self, request):
        try:
            self._requestPath = "/panorama/v2/user"
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request._serialize()
            print("params", params)
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def del_user(self, request):
        try:
            self._requestPath = "/panorama/v2/user/delete"
            self.httpProfile.reqMethod = "DELETE"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request._serialize()
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def get_roles(self):
        try:
            self._requestPath = "/panorama/v2/roles"
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = ""
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)