# -*- coding: UTF-8 -*-

import sys
import os

class PermissionService(object):

    @classmethod
    async def create_permission(cls, szName, szDescription):
        pass

    @classmethod
    async def select_permission(cls, szName):
        pass

    @classmethod
    async def user_has_permission(cls, szUser, szPermission):
        pass

    @classmethod
    async def group_has_permission(cls, szUser, szPermission):
        pass

    @classmethod
    async def grant_permission_to_user(cls, szPermission, szUser):
        pass

    @classmethod
    async def grant_permissions_to_user(cls, lstPermission, szUser):
        pass

    @classmethod
    async def grant_permission_to_group(cls, szPermission, szGroup):
        pass

    @classmethod
    async def grant_permissions_to_group(cls, lstPermission, szGroup):
        pass

    @classmethod
    async def check_user_permission(cls, szUser, szPermission):
        pass

    @classmethod
    async def check_user_permissions(cls, szUser, lstPermission):
        pass

    @classmethod
    async def check_group_permission(cls, szGroup, szPermission):
        pass

    @classmethod
    async def check_group_permissions(cls, szGroup, lstPermission):
        pass