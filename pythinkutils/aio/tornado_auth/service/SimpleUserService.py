# -*- coding: UTF-8 -*-

import sys
import os

from pythinkutils.aio.tornado_auth.service.BaseUserService import BaseUserService

class SimpleUserService(BaseUserService):

    @classmethod
    async def create_user(cls, szUserName, szPwd, nSuperUser=0, nActive=1):
        pass

    @classmethod
    async def change_password(cls, szUserName, szPwd):
        pass

    @classmethod
    async def login(cls, szUserName, szPwd):
        pass