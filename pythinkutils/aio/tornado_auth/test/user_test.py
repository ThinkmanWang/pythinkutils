# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.tornado_auth.service.SimpleUserService import SimpleUserService
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_query_user_by_name():
    dictRet = await SimpleUserService.get_user("root")
    g_logger.info(dictRet)
    g_logger.info(obj2json(dictRet))

async def test_query_user_id_name():
    dictRet = await SimpleUserService.get_user_id("root")
    g_logger.info(dictRet)

async def test_user_token():
    ret = await SimpleUserService.check_token("root", "00000000000000000000000000000000")
    g_logger.info(ret)
    ret = await SimpleUserService.check_token("root", "00000000000000000000000000000001")
    g_logger.info(ret)

async def test_create_user():
    ret = await SimpleUserService.create_user("root", "123456")
    g_logger.info(ret)

    ret = await SimpleUserService.create_user("user1", "123456")
    g_logger.info(ret)

    ret = await SimpleUserService.change_password("user1", "12345678")
    g_logger.info(ret)

async def test_login():
    ret = await SimpleUserService.login("root", "Ab123145")
    g_logger.info(ret)

async def test():
    # await test_query_user_by_name()
    # await test_query_user_id_name()
    # await test_user_token()
    # await test_create_user()
    await test_login()

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()