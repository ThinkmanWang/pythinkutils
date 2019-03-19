# -*- coding: UTF-8 -*-

import sys
import os
import abc

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.common.StringUtils import *

class BaseSimpleAuthHandler(tornado.web.RequestHandler):

    @abc.abstractmethod
    async def on_goto_login_page(self):
        pass

    async def login(self, szUsername, szPwd):
        from pythinkutils.aio.tornado_auth.service.SimpleUserService import SimpleUserService

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

def login_required():
    def auth_decorator(func):
        async def inner(self, *args, **kwargs):
            if is_empty_string(self.get_cookie("username")) or is_empty_string(self.get_cookie("token")):
                await self.on_goto_login_page()
            else:
                await func(self, *args, **kwargs)
        return inner
    return auth_decorator
