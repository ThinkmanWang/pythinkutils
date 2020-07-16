# -*- coding: utf-8 -*-
import sys
import os
import asyncio

import tornado.ioloop

from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from tornado import gen
import random

# from pythinkutils.aio.common.aiolog import g_aio_logger

ENCODING = "utf-8"
EOF = b"\r\n"


async def echo(stream):
    print("start echo")
    # while stream is not None \
    #         and stream.closed() is False:
    while True:
        try:
            byteData = await stream.read_until(EOF)
            szText = byteData.decode(ENCODING)

            print("reply>>> " + szText)

        except Exception as ex:
            pass

async def test1():
    while True:
        await asyncio.sleep(1)
        print("FXXK")

async def send(stream):
    print("start send")
    asyncio.ensure_future(test1())

    try:
        while True:
            await asyncio.sleep(1)
            szData = str(random.randint(1, 100))
            print("send>>> " + szData)

            if szData is None or len(szData.strip()) <= 0:
                return

            await stream.write(szData.encode(ENCODING))
            await stream.write(EOF)

    except KeyboardInterrupt:
        stream.close()

async def run_client():
    stream = await TCPClient().connect('127.0.0.1', 8888)
    await asyncio.gather(send(stream), echo(stream))

def main():
    loop = asyncio.get_event_loop()
    asyncio.gather(run_client())
    loop.run_forever()

if __name__ == '__main__':
    main()