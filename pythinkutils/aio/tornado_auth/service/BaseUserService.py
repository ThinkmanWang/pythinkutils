# -*- coding: UTF-8 -*-

import sys
import os
import abc

import aiomysql

from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger

class BaseUserService(object):

    @classmethod
    async def get_user(cls, szUserName):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_user "
                                          "WHERE "
                                          "  username = %s "
                                          "LIMIT 1 ", (szUserName, ))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        return rows[0]
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def get_user_id(cls, szUserName):
        pass

    @classmethod
    @abc.abstractmethod
    async def create_user(cls, szUserName, szPwd, nSuperUser = 0, nActive = 1):
        pass

    @classmethod
    @abc.abstractmethod
    async def change_password(cls, szUserName, szPwd):
        pass

    @classmethod
    @abc.abstractmethod
    async def login(cls, szUserName, szPwd):
        pass

    @classmethod
    async def check_token(cls, szUserName, szToken):
        pass