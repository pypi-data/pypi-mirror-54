import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie


class DataSetClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''

    def get_dataset(self):
        try:
            self._requestPath = "/panorama/v2/dataset/list"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = ""
            self._default_token = c.get_cookie()
            body, resp_header = self.call(params)
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

    def del_dataset(self, request):
        try:
            self._requestPath = "/panorama/v2/dataset/delete"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "DELETE"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = ""
            self._requestPath += "/%s" % request.id
            self._default_token = c.get_cookie()
            body, resp_header = self.call(params)
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

    def del_dataset_data(self, request):
        try:
            self._requestPath = "/panorama/v2/dataset/delete/dgraph"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "DELETE"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = ""
            self._requestPath += "/%s" % request.id
            self._default_token = c.get_cookie()
            body, resp_header = self.call(params)
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

    def add_dataset(self, request):
        try:
            self._requestPath = "/panorama/v2/dataset"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {}
            header["Panorama-Source-Guid"] = self._panorama_source_guid
            header["Panorama-Workspace-Id"] = self._panorama_workspace_id
            params = request.to_json_string()
            self._default_token = c.get_cookie()
            body, resp_header = self.call(params, header)
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