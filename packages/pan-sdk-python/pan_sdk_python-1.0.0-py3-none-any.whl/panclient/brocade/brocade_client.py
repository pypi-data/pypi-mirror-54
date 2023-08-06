import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie
from panclient.brocade import models


# /panorama/v2/brocade/list/rawQuery
class BrocadeClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''
    _panorama_source_guid = None
    _panorama_workspace_id = None

    def new_brocade(self, request):
        try:
            self._requestPath = "/panorama/v2/brocade/new"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            # header = {"Panorama-Source-Guid": self._panorama_source_guid, "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request.to_json_string()
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "创建锦囊错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def delete_brocade(self, request):
        try:
            self._requestPath = "/panorama/v2/brocade/delete/"
            # self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "DELETE"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = ""
            self._requestPath += request.brocadeId
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "删除锦囊错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    # 获取锦囊列表
    def get_brocade_list(self):
        try:
            self._requestPath = "/panorama/v2/brocade/list"
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
                message = "获取锦囊列表错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def generate_endpoint(self, request):
        try:
            self._requestPath = "/panorama/v5/apis/generate/url"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid, "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request._serialize()
            self._default_token = c.get_cookie()
            body, header = self.call(params, header)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "锦囊生成Endpoint错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def api_release(self, request):
        try:
            self._requestPath = "/panorama/v5/apis/release"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid, "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request.to_json_string()
            self._default_token = c.get_cookie()
            body, header = self.call(params, header)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "锦囊生成API错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)

    def get_raw_query_list(self):
        try:
            self._requestPath = "/panorama/v2/brocade/list/rawQuery"
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

    def raw_query_exec(self, request):
        try:
            self._requestPath = "/panorama/dgraph/proxyapi/query"
            self._default_content_type = 'text/plain'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            params = request.content
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "运行query错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)


