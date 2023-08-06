import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie
from panclient.schema import models


class SchemaClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''
    _panorama_source_guid = None
    _panorama_workspace_id = None

    def get_schema(self):
        try:
            self._requestPath = "/panorama/v2/schema"
            self._default_content_type = 'application/x-www-form-urlencoded'
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

    def mod_schema_concept(self, request):
        try:
            self._requestPath = "/panorama/v2/schema/concept"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid, "Panorama-Workspace-Id": self._panorama_workspace_id}
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

    def get_all_db_table(self):
        try:
            self._requestPath = "/panorama/import/getAllDBAndTable"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Workspace-Id": self._panorama_workspace_id}
            params = ""
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

    def auto_mapping(self, request):
        try:
            self._requestPath = "/panorama/import/autoMapping"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            request.header["Panorama-Workspace-Id"] = self._panorama_workspace_id
            params = request._serialize()
            self._default_token = c.get_cookie()
            body, resp_header = self.call(params, request.header)
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

    def create_system_schema(self, request):
        try:
            self._requestPath = "/panorama/import/createSystemSchema"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request._serialize()
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