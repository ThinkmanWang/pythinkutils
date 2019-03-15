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

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test_query_user_by_name())

    loop.run_forever()

if __name__ == '__main__':
    main()