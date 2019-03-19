# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.tornado_auth.service.GroupService import GroupService
from pythinkutils.aio.tornado_auth.service.PermissionService import PermissionService

from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_create_permission():
    await PermissionService.create_permission("permission_read_user_info")
    await PermissionService.grant_permission_to_user("permission_read_user_info", "root")
    await PermissionService.grant_permission_to_group("permission_read_user_info", 10000001)

async def test_has_permission():
    bHasPermission = await PermissionService.user_has_permission("root", "permission_read_user_info")
    g_logger.info(bHasPermission)

async def group_has_permission():
    bHasPermission = await PermissionService.group_has_permission(10000001, "permission_read_user_info")
    g_logger.info(bHasPermission)

async def test():
    await test_create_permission()
    await test_has_permission()
    await group_has_permission()

def main():
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()