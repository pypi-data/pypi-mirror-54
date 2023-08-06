import json

from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.abstract_client import AbstractClient
from panclient.common.cookie import cookie
from panclient.workflow import models


class WorkflowClient(AbstractClient):
    _apiVersion = '2018-06-06'
    _endpoint = '192.168.31.149:8089'
    _requestPath = None
    _default_content_type = 'application/x-www-form-urlencoded'
    _default_token = ''
    _panorama_source_guid = None
    _panorama_workspace_id = None

    def get_graph_product(self, request):
        try:
            self._requestPath = "/panorama/product/GraphProduct"
            self.httpProfile.reqMethod = "GET"
            self.httpProfile.keepAlive = 30
            params = request._serialize()
            c = cookie.Cookie()
            print(c.get_cookie())
            self._default_token = c.get_cookie()
            #header = {"Panorama-Workspace-Id": self._panorama_workspace_id}
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

    def sem_set(self, request):
        try:
            self._requestPath = "/semset"
            self._default_content_type = 'application/json'
            self.httpProfile.reqMethod = "POST"
            self.httpProfile.keepAlive = 30
            params = b"["
            for sm in request.SemSetList:
                params += sm.to_json_string() + b", "
            params = params[:-2]
            params += b"]"
            print(params)
            c = cookie.Cookie()
            print(c.get_cookie())
            self._default_token = c.get_cookie()
            body, header = self.call(params)
            print("body:", body)
            return body
        except Exception as e:
            if isinstance(e, PanSDKException):
                raise
            else:
                raise PanSDKException(e.code, e.message)