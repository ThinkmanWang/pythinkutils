# -*- coding: UTF-8 -*-

import sys
import os

class GroupService(object):

    @classmethod
    async def create_group(cls, szGroupName):
        pass

    @classmethod
    async def get_group(cls, szGroupName):
        pass

    @classmethod
    async def get_group_id(cls, szGroupName):
        pass

    @classmethod
    async def change_group_name(cls, szGroupName, szNewGroupName):
        pass

    @classmethod
    async def get_group_members(cls, szGroupName):
        pass

    @classmethod
    async def add_user_to_group(cls, szUserName, szGroupName):
        pass