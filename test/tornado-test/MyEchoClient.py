# -*- coding: utf-8 -*-
import sys
import os
import asyncio

import tornado.ioloop

from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from tornado import gen

# from pythinkutils.aio.common.aiolog import g_aio_logger

ENCODING = "utf-8"

async def echo(stream, text):
    if text is None or len(text.strip()) <= 0:
        return

    byteStr = text.encode(ENCODING)
    # print(type(text))
    # print(type(byteStr))

    await stream.write(text.encode(ENCODING))
    await stream.write(b"\r\n")

    byteData = await stream.read_until(b"\r\n")
    szText = byteData.decode(ENCODING)
    print("reply>>> " + szText)

async def run_client():
    stream = await TCPClient().connect('127.0.0.1', 8888)
    try:
        while True:
            szData = input('echo>>> ')
            await echo(stream, szData)
    except KeyboardInterrupt:
        stream.close()


async def main():
    await run_client()

if __name__ == '__main__':
    asyncio.run(main())