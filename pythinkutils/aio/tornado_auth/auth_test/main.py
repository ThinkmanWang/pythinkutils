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

class MainHandler(tornado.web.RequestHandler):

    async def get(self):
        self.write("To be continued...")

class LoginHandler(tornado.web.RequestHandler):

    async def get(self):
        self.write("To be continued...")

application = tornado.web.Application(handlers = [
    (r"/login", LoginHandler)
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