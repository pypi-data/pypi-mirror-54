import copy
import re
import json
import sys
import warnings

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import panclient
from panclient.common.exception.pan_sdk_exception import PanSDKException
from panclient.common.http.request import ApiRequest
from panclient.common.http.request import RequestInternal
from panclient.common.profile.http_profile import HttpProfile

warnings.filterwarnings("ignore")

_json_content = 'application/json'
_text_plain_content = 'text/plain'
_multipart_content = 'multipart/form-data'
_form_urlencoded_content = 'application/x-www-form-urlencoded'


class AbstractClient(object):
    _requestPath = '/'
    _params = {}
    _apiVersion = ''
    _endpoint = ''
    _sdkVersion = 'SDK_PYTHON_%s' % panclient.__version__
    _default_content_type = _form_urlencoded_content
    _default_token = ''

    def __init__(self, profile=None):
        self.httpProfile = HttpProfile() if profile is None else profile
        self.request = ApiRequest(self._get_endpoint(), self.httpProfile.reqTimeout)
        if self.httpProfile.keepAlive:
            self.request.set_keep_alive()

    def _fix_params(self, params):
        if not isinstance(params, (dict,)):
            return params
        return self._format_params(None, params)

    def _format_params(self, prefix, params):
        d = {}
        if params is None:
            return d

        if not isinstance(params, (tuple, list, dict)):
            d[prefix] = params
            return d

        if isinstance(params, (list, tuple)):
            for idx, item in enumerate(params):
                if prefix:
                    key = "{0}.{1}".format(prefix, idx)
                else:
                    key = "{0}".format(idx)
                d.update(self._format_params(key, item))
            return d

        if isinstance(params, dict):
            for k, v in params.items():
                if prefix:
                    key = '{0}.{1}'.format(prefix, k)
                else:
                    key = '{0}'.format(k)
                d.update(self._format_params(key, v))
            return d

        raise PanSDKException("ClientParamsError", "some params type error")

    # it must return bytes instead of string
    def _get_multipart_body(self, params, boundary, options=None):
        if options is None:
            options = {}
        # boundary and params key will never contain unicode characters
        boundary = boundary.encode()
        binparas = options.get("BinaryParams", [])
        body = b''
        for k, v in params.items():
            kbytes = k.encode()
            body += b'--%s\r\n' % boundary
            body += b'Content-Disposition: form-data; name="%s"' % kbytes
            if k in binparas:
                body += b'; filename="%s"\r\n' % kbytes
            else:
                body += b"\r\n"
                if isinstance(v, list) or isinstance(v, dict):
                    v = json.dumps(v)
                    body += b'Content-Type: application/json\r\n'
            if sys.version_info[0] == 3 and isinstance(v, type("")):
                v = v.encode()
            body += b'\r\n%s\r\n' % v
        if body != b'':
            body += b'--%s--\r\n' % boundary
        return body

    def _check_status(self, resp_inter):
        if resp_inter.status != 200:
            raise PanSDKException("ServerNetworkError", resp_inter.data)

    def _get_endpoint(self):
        endpoint = self.httpProfile.endpoint
        if endpoint is None:
            endpoint = self._endpoint
        return endpoint

    def call(self, params, header=None):
        endpoint = self._get_endpoint()
        req_inter = RequestInternal(endpoint,
                                    self.httpProfile.reqMethod,
                                    self._requestPath,
                                    header)
        self._build_req_inter(params, req_inter)
        print(req_inter)
        resp_inter = self.request.send_request(req_inter)
        print(resp_inter)
        self._check_status(resp_inter)
        data = resp_inter.data
        if sys.version_info[0] > 2:
            data = data.decode()
        else:
            data = data.decode('UTF-8')
        return data, resp_inter.header

    def raw_call(self, params, header=None):
        endpoint = self._get_endpoint()
        req_inter = RequestInternal(endpoint,
                                    self.httpProfile.reqMethod,
                                    self._requestPath,
                                    header)
        self._build_req_inter(params, req_inter)
        print(req_inter)
        resp_inter = self.request.send_request(req_inter)
        print(resp_inter)
        self._check_status(resp_inter)
        data = resp_inter.data
        if sys.version_info[0] > 2:
            data = data.decode()
        else:
            data = data.decode('UTF-8')
        return data, resp_inter.header

    def _build_req_inter(self,  params, req):
        self._build_req(params, req)

    def _build_req(self,  params, req):
        params = copy.deepcopy(self._fix_params(params))

        if self._default_content_type == _form_urlencoded_content:
            req.header["Content-Type"] = self._default_content_type
            req.data = urlencode(params)
            req.data = re.sub(".[0-9][0-9]{0,1}=", "%5B%5D=", req.data)
        elif self._default_content_type == _json_content:
            req.header["Content-Type"] = self._default_content_type
            req.data = params
        elif self._default_content_type == _text_plain_content:
            req.header["Content-Type"] = self._default_content_type
            req.data = params
        elif self._default_content_type == _multipart_content:
            req.data = params
        req.header["Cookie"] = self._default_token

