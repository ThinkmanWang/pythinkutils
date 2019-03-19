# -*- coding: UTF-8 -*-

import sys
import os

import aiomysql

from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class GroupService(object):

    @classmethod
    async def create_group(cls, szGroup, nOwner = 10000001, szDesc = ""):
        dictGroup = await cls.get_group(szGroup, nOwner)
        if dictGroup is not None:
            if dictGroup["owner"] == nOwner:
                return dictGroup

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_group(owner, `name`, description) "
                                          "VALUES "
                                          "  (%s, %s, %s)"
                                          , (nOwner, szGroup, szDesc))

                        await conn.commit()

                        dictRet = await cls.get_group(szGroup)
                        return dictRet
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def get_group(cls, szGroup, nOwner = 10000001):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_group "
                                          "WHERE "
                                          "  `name` = %s "
                                          "  AND owner = %s "
                                          "LIMIT 1 ", (szGroup, nOwner))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        rows[0]["members"] = await cls.get_group_members(szGroup)
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
    async def get_group_id(cls, szGroup, nOwner = 10000001):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_group "
                                          "WHERE "
                                          "  `name` = %s "
                                          "  AND owner = %s "
                                          "LIMIT 1 ", (szGroup, nOwner))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        return rows[0]["id"]
                except Exception as e:
                    g_logger.error(e)
                    return -1
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return -1

    @classmethod
    async def change_group_name(cls, szGroup, szNewGroupName, nOwner = 10000001):
        nID = await cls.get_group_id(szGroup, nOwner)
        if nID <= 0:
            return None

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("UPDATE t_thinkauth_group "
                                          "  set `name` = %s "
                                          "WHERE "
                                          "  id = %s "
                                          , (szNewGroupName, nID))

                        await conn.commit()

                        dictRet = await cls.get_group(szGroup)
                        return dictRet
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def get_group_members(cls, szGroup, nOwner = 10000001):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT                                                   "
                                          "	 c.*                                                    "
                                          "FROM                                                     "
                                          "	 t_thinkauth_user_group as a                            "
                                          "	 left JOIN t_thinkauth_group as b on a.group_id = b.id  "
                                          "	 LEFT JOIN t_thinkauth_user as c on a.user_id = c.id    "
                                          "WHERE                                                    "
                                          "	 b.`name` = %s                                          "
                                          "  AND owner = %s ", (szGroup, nOwner))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return []

                        return rows
                except Exception as e:
                    g_logger.error(e)
                    return []
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return []

    @classmethod
    async def add_user_to_group(cls, szUserName, szGroup, nOwner = 10000001):
        from pythinkutils.aio.tornado_auth.service.BaseUserService import BaseUserService
        nUID = await BaseUserService.get_user_id(szUserName)
        if nUID < 0:
            return False

        dictGroup = await cls.get_group(szGroup, nOwner)
        if dictGroup is None:
            return False

        nGID = dictGroup["id"]
        if nGID < 0:
            return False

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_user_group(user_id, group_id) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (nUID, nGID))

                        await conn.commit()

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return True
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return True

    @classmethod
    async def delete_group(cls, szGroup, nOwner = 10000001):
        pass