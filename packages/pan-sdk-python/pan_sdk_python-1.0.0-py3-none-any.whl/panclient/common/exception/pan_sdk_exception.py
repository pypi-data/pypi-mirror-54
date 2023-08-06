# -*- coding: utf-8 -*-

import sys


class PanSDKException(Exception):
    """panapi sdk 异常类"""

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __str__(self):
        s = "[PanSDKException] code:%s message:%s" % (
            self.code, self.message)
        if sys.version_info[0] < 3 and isinstance(s):
            return s.encode("utf8")
        else:
            return s

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message
