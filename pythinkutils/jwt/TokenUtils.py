# -*- coding: utf-8 -*-

import requests
import json
import jwt
import redis

from pythinkutils.common.log import g_logger
from pythinkutils.config.Config import g_config
from pythinkutils.common.object2json import *
from pythinkutils.redis.ThinkRedis import ThinkRedis

class TokenUtils:

    g_szHost = g_config.get("auth", "host")
    JWT_SALT = ""

    @classmethod
    def auth_token(cls, szAppId, szSecret):
        try:
            szUrl = "{}{}".format(TokenUtils.g_szHost, "/ruoyi-api/auth/token")
            resp = requests.post(szUrl, data={"appid": szAppId, "secret": szSecret})

            if 200 != resp.status_code:
                return None

            dictRet = json.loads(resp.text)
            if 200 != dictRet["code"]:
                return None

            return dictRet["token"]
        except Exception as ex:
            g_logger.error(ex)
            return None

    @classmethod
    def get_info(cls, szToken):
        try:
            szUrl = "{}{}".format(TokenUtils.g_szHost, "/ruoyi-api/getInfo")
            dictHeader = {
                "Authorization": "Bearer {}".format(szToken)
            }

            resp = requests.get(szUrl, headers = dictHeader)
            if 200 != resp.status_code:
                return None

            dictRet = json.loads(resp.text)
            if 200 != dictRet["code"]:
                return None

            return dictRet
        except Exception as ex:
            g_logger.error(ex)
            return None

    @classmethod
    def parse_token(cls, szToken):
        try:
            jwt_options = {
                'verify_signature': False,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': True,
                'verify_aud': False
            }

            dictToken = jwt.decode(szToken, TokenUtils.JWT_SALT, algorithms=["HS512"], options=jwt_options)
            return dictToken
        except Exception as ex:
            g_logger.error(ex)
            return None

    @classmethod
    def expire_time(cls, szToken):
        try:
            dictToken = cls.parse_token(szToken)
            if dictToken is None:
                return 0

            r = redis.StrictRedis(connection_pool=ThinkRedis.get_conn_pool_ex())

            szKey = "login_tokens:{}".format(dictToken["login_user_key"])
            return r.ttl(szKey)

        except Exception as ex:
            g_logger.error(ex)
            return None


# szToken = TokenUtils.auth_token("1234", "5678")
# g_logger.info(szToken)
#
# dictRet = TokenUtils.get_info(szToken)
# g_logger.info(obj2json(dictRet))
#
# g_logger.info(obj2json(TokenUtils.parse_token(szToken)))
# g_logger.info(TokenUtils.expire_time(szToken))

