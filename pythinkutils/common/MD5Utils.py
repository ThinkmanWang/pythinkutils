# -*- coding: UTF-8 -*-

import sys
import os

import hashlib

class MD5Utils(object):

    @classmethod
    def md5(cls, szText):
        m = hashlib.md5()
        m.update(szText.encode("utf8"))
        print(m.hexdigest())
        return m.hexdigest()


# print(MD5Utils.md5("123456").lower())
