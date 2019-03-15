# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.tornado_auth.service.SimpleUserService import SimpleUserService
from pythinkutils.common.object2json import *

async def test_query_user_by_name():
    dictRet = await SimpleUserService.get_user("root")
    print(dictRet)
    print(obj2json(dictRet))

async def test_query_user_id_name():
    dictRet = await SimpleUserService.get_user_id("root")
    print(dictRet)

async def test_user_token():
    ret = await SimpleUserService.check_token("root", "00000000000000000000000000000000")
    print(ret)
    ret = await SimpleUserService.check_token("root", "00000000000000000000000000000001")
    print(ret)

async def test():
    await test_query_user_by_name()
    await test_query_user_id_name()
    await test_user_token()

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()