import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie
from panclient.workspace import models


class WorkspaceClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''
    _panorama_source_guid = None
    _panorama_workspace_id = None

    def get_all_product(self):
        try:
            self._requestPath = "/panorama/product/all"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            self._requestPath += "?workspaceId=%s" % self._panorama_workspace_id
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

    def create_product(self, request):
        try:
            self._requestPath = "/panorama/v2/analysis/new"
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

    def mod_product(self, request):
        try:
            self._requestPath = "/panorama/product"
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

    def del_product(self, request):
        try:
            self._requestPath = "/panorama/product"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "DELETE"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid,
                      "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request._serialize()
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

    def get_product(self, request):
        try:
            self._requestPath = "/panorama/product"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid, "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request._serialize()
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

    #/panorama/product/graph/vertices/update
    def update_product_graph_vertices(self, request):
        try:
            self._requestPath = "/panorama/product/graph/vertices/update"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid,
                      "Panorama-Workspace-Id": self._panorama_workspace_id}
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

    # /panorama/vertex/multiple
    def get_vertex_multiple(self, request):
        try:
            self._requestPath = "/panorama/vertex/multiple"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid}
            params = request._serialize()
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

    # panorama/product/graph/vertices/remove
    def delete_graph_vertices(self, request):
        try:
            self._requestPath = "/panorama/product/graph/vertices/remove"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid,
                      "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request._serialize()
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

    # find relate /panorama/vertex/find-related
    def find_vertex_related(self, request):
        try:
            self._requestPath = "/panorama/vertex/find-related"
            self._default_content_type = 'application/x-www-form-urlencoded'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Source-Guid": self._panorama_source_guid,
                      "Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request._serialize()
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

    # search  /panorama/v2/search
    def search(self, request):
        try:
            self._requestPath = "/panorama/v2/search"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            c = cookie.Cookie()
            header = {"Panorama-Workspace-Id": self._panorama_workspace_id}
            params = request.to_json_string()
            self._default_token = c.get_cookie()
            body, header = self.call(params, header)
            print("body:", body)
            response = json.loads(body)
            if response:
                return body
            else:
                code = "False"
                message = "运行search错误"
                raise PanSDKException(code, message)
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)