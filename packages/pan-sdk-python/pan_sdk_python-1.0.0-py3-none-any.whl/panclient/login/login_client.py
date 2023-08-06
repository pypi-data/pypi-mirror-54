import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.login import models
from panclient.common.cookie import cookie


class LoginClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token =  ''

    def login(self, request):
        try:
            self._requestPath = "/panorama/login"
            _default_content_type = 'application/x-www-form-urlencoded'
            params = request._serialize()
            body, header = self.call(params)
            token = header.get("Set-Cookie")
            response = json.loads(body)
            if response["success"]:
                model = models.CreateLoginResponse()
                model._deserialize(response)
                c = cookie.Cookie()
                c.set_cookie(token)
                return model
            else:
                code = "False"
                message = response["message"]
                c = cookie.Cookie()
                c.clear_cookie()
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def logout(self):
        try:
            self._requestPath = "/panorama/logout"
            params = ""
            c = cookie.Cookie()
            print(c.get_cookie())
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            c.clear_cookie()
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = response["message"]
                c = cookie.Cookie()
                c.clear_cookie()
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)