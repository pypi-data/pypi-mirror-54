#!/usr/bin/python
# -*- coding: utf-8 -*-


class Cookie(object):

    def set_cookie(self, cookie):
        f = open('cookie', 'w')
        f.write(cookie)
        f.close()

    def get_cookie(self):
        f = open('cookie', 'r')
        cookie = f.readline(-1)
        f.close()
        return cookie

    def clear_cookie(self):
        f = open('cookie', 'w')
        f.write("")
        f.close()