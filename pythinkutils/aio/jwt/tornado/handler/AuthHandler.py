# -*- coding: utf-8 -*-

from pythinkutils.aio.jwt.tornado.handler.BaseHandler import BaseHandler
from pythinkutils.common.StringUtils import *

class AuthHandler(BaseHandler):
    async def create_token(self, szAppId, szSecret):
        pass

    async def token_valid(self):
        pass

    async def get_uid_name(self):
        pass

    async def get_userinfo(self):
        pass

    async def get_token(self):
        pass

    async def get_permission_list(self):
        pass