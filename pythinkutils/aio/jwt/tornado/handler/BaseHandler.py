# -*- coding: utf-8 -*-

import sys
import os
import abc
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def get_uid(self):
        pass

    async def get_userinfo(self):
        pass

    async def get_token(self):
        pass

    async def get_permission_list(self):
        pass
