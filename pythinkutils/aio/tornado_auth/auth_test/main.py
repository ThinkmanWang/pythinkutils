# -*- coding: UTF-8 -*-

import sys
import os

# -*- coding: UTF-8 -*-

import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import aiomysql

from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

from pythinkutils.common.log import g_logger
from pythinkutils.aio.tornado_auth.handler.BaseSimpleAuthHandler import BaseSimpleAuthHandler, login_required, permission_required
from pythinkutils.common.StringUtils import *

class LoginHandler(BaseSimpleAuthHandler):

    async def on_goto_login_page(self):
        g_logger.info("Goto login page")
        await self.get()

    async def post(self):
        await self.get()

    async def get(self):
        szUsername = self.get_argument("username", "")
        szPwd = self.get_argument("password", "")
        szRedirectUrl = self.get_argument("redirect_url", "")

        if is_empty_string(szUsername) or is_empty_string(szPwd):
            self.write('''
            <form action="/login" method="GET">
                <p>Username: <input type="text" name="username" /></p>
                <p>Password: <input type="text" name="password" /></p>
                <p>Password: <input type="text" name="redirect_url" value="{}" /></p>
                <input type="submit" value="Submit" />
            </form>
            '''.format(szRedirectUrl))
        else:
            _szUsername, szToken = await self.login(szUsername, szPwd)
            if False == is_empty_string(szToken):
                if is_empty_string(szRedirectUrl):
                    self.redirect("/")
                else:
                    self.redirect(szRedirectUrl)
            else:
                self.redirect("/login")

class FxxkHandler(BaseSimpleAuthHandler):

    async def on_goto_login_page(self):
        g_logger.info("Goto login page")
        self.redirect("/login?redirect_url=%2ffxxk")

    @permission_required("permission_hehe")
    async def get(self):
        self.write("FxxkHandler To be continued...")

class MainHandler(BaseSimpleAuthHandler):

    async def on_goto_login_page(self):
        g_logger.info("Goto login page")
        self.redirect("/login")

    @login_required()
    async def get(self):
        self.write("HOMEPAGE To be continued...")

application = tornado.web.Application(handlers = [
    (r"/login", LoginHandler)
    , (r"/fxxk", FxxkHandler)
    , (r'/', MainHandler)
], autoreload=False)

async def on_server_started():
    g_logger.info("Server Started")

if __name__ == '__main__':

    http_server = HTTPServer(application)
    http_server.bind(8590)
    http_server.start(0)

    # ipDB = IPLocation.instance()
    g_logger.info('HTTP Server started... %d' % (os.getpid(),))

    tornado.platform.asyncio.AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()

    asyncio.gather(on_server_started())

    ioloop.run_forever()