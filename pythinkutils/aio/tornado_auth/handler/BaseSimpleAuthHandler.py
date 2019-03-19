# -*- coding: UTF-8 -*-

import sys
import os
import abc

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.aio.tornado_auth.service.SimpleUserService import SimpleUserService
from pythinkutils.common.StringUtils import *

class BaseSimpleAuthHandler(tornado.web.RequestHandler):

    @abc.abstractmethod
    async def on_goto_login_page(self):
        pass

    async def login(self, szUsername, szPwd):
        nExpireDays = 180

        szToken = await SimpleUserService.login(szUsername, szPwd, nExpireDays)
        if is_empty_string(szToken):
            return (szUsername, None)

        self.set_cookie("username", szUsername, expires_days = nExpireDays)
        self.set_cookie("token", szToken, expires_days = nExpireDays)

        return (szUsername, szToken)

    async def logout(self):
        self.clear_cookie("username")
        self.clear_cookie("token")

    async def login_required(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if is_empty_string(self.get_cookie("username")) or is_empty_string(self.get_cookie("token")):
                    self.on_goto_login_page()

                return func(*args, **kwargs)

            return wrapper

        return decorator