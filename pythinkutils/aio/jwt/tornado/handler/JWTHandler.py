# -*- coding: utf-8 -*-

from pythinkutils.aio.jwt.tornado.handler.AuthHandler import AuthHandler
from pythinkutils.common.StringUtils import *

class JWTHandler(AuthHandler):

    async def auth_token(self, szAppId, szSecret):
        from pythinkutils.aio.jwt.TokenUtils import TokenUtils

        return await TokenUtils.auth_token(szAppId, szSecret)

    async def token_valid(self):
        from pythinkutils.aio.jwt.TokenUtils import TokenUtils

        szToken = self.get_token()
        if is_empty_string(szToken):
            return False

        nExpire = await TokenUtils.expire_time(szToken)
        return nExpire > 0

    async def get_uid_name(self):
        try:
            dictUser = await self.get_userinfo()
            if dictUser is None:
                return None, None

            return dictUser["user"]["userId"], dictUser["user"]["userName"]
        except Exception as e:
            return None, None

    async def get_userinfo(self):
        from pythinkutils.aio.jwt.TokenUtils import TokenUtils

        szToken = self.get_token()
        if is_empty_string(szToken):
            return None

        return await TokenUtils.get_info(szToken)

    async def get_token(self):
        szAuth = self.request.headers.get("Authorization")
        if is_empty_string(szAuth):
            return None

        lstItem = szAuth.split(" ")
        if lstItem is None or len(lstItem) <= 0 or "Bearer" != lstItem[0].strip():
            return None

        return lstItem[1]

    async def get_permission_list(self):
        try:
            dictUser = await self.get_userinfo()
            if dictUser is None:
                return None

            return dictUser["permissions"]
        except Exception as e:
            return None, None