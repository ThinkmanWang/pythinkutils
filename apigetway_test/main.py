# -*- coding: utf-8 -*-
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
from pythinkutils.aio.jwt.tornado.handler.BaseHandler import BaseHandler
from pythinkutils.aio.jwt.tornado.handler.JWTHandler import JWTHandler
from pythinkutils.common.StringUtils import *
from pythinkutils.common.object2json import obj2json

class MainHandler(BaseHandler):
    async def post(self):
        self.write("HOMEPAGE To be continued...")

    async def get(self):
        await self.post()

class AuthHandler(JWTHandler):

    async def post(self):
        dictToken = await self.create_token(self.get_argument("appid"), self.get_argument("secret"))

        if dictToken is None:
            return obj2json({"code": 500, "msg": "Server Error"})

        self.write(obj2json(dictToken))

    async def get(self):
        await self.post()

async def on_server_started():
    g_logger.info("Server Started!!!")

application = tornado.web.Application(handlers = [
    (r"/auth/token", AuthHandler)
    , (r"/", MainHandler)
], cookie_secret="BUEa2ckrQtmBofim3aP6cwr/acg0LEu6mHUxq4O3EY0=", autoreload=False)

if __name__ == '__main__':

    http_server = HTTPServer(application)

    http_server.bind(8080)
    http_server.start(0)
    # http_server.listen(8080)


    # ipDB = IPLocation.instance()
    g_logger.info('HTTP Server started... %d' % (os.getpid(),))
    asyncio.gather(on_server_started())

    tornado.ioloop.IOLoop.current().start()

    # tornado.platform.asyncio.AsyncIOMainLoop().install()
    # AsyncIOMainLoop().install()
    # ioloop = asyncio.get_event_loop()
    #
    # asyncio.gather(on_server_started())
    #
    # ioloop.run_forever()