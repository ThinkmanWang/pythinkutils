# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.tornado_auth.service.GroupService import GroupService
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_get_group():
    dictRet = await GroupService.get_group("admin")
    if dictRet is None:
        g_logger.info("FXXK")
        return

    g_logger.info(obj2json(dictRet))


async def test():
    await test_get_group()

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()