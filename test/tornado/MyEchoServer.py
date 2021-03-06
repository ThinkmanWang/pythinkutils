# -*- coding: utf-8 -*-

import sys
import os
import asyncio

import tornado.ioloop

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen

from pythinkutils.aio.common.aiolog import g_aio_logger

class TCPConnection(object):

    def __init__(self, stream, address):
        self.__stream = stream
        self.__address = address

        asyncio.gather(self.on_start())
        self.__stream.set_close_callback(self.on_close)

    def on_close(self):
        if self.__stream is not None \
                and self.__stream.closed() is False:
            self.__stream.close()
            self.__stream = None

    async def on_start(self):
        while self.__stream is not None \
                and self.__stream.closed() is False:
            try:
                byteData = await self.__stream.read_until(MyEchoServer.EOF)
                szText = byteData.decode(MyEchoServer.ENCODING)

                await g_aio_logger.info(szText)

                self.__stream.write(byteData)
            except Exception as ex:
                pass

        await g_aio_logger.info("Connection closed!!!")

class MyEchoServer(TCPServer):
    ENCODING = "utf-8"
    EOF = b"\r\n"

    async def handle_stream(self, stream, address):
        TCPConnection(stream, address)
        await g_aio_logger.info("Listening...")


def main():
    server = MyEchoServer()
    server.listen(8888)
    # server.bind(8888)
    # server.start(0)  # Forks multiple sub-processes

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()