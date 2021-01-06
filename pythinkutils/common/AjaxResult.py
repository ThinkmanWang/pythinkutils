# -*- coding: utf-8 -*-

class AjaxResult:
    def __init__(self, code=200, msg="", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def error(cls):
        return AjaxResult(500, "Server Error")