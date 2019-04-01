# -*- coding: UTF-8 -*-

import sys
import os

import aiomysql

from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class PermissionService(object):
    @classmethod
    async def create_permission(cls, szName, szDescription=""):
        dictPermission = await cls.select_permission(szName)
        if dictPermission is not None:
            return dictPermission

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_permission(`permission_name`, description) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (szName, szDescription))

                        await conn.commit()

                        dictRet = await cls.select_permission(szName)
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
    async def select_permission(cls, szName):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_permission "
                                          "WHERE "
                                          "  `permission_name` = %s "
                                          "   "
                                          "LIMIT 1 ", (szName,))

                        rows = await cur.fetchall()
                        if rows is None or len(rows) <= 0:
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
    async def user_has_permission(cls, nUID, nPID):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute(
                            "SELECT                                                                       "
                            "	1                                                                           "
                            "WHERE                                                                        "
                            "	EXISTS (                                                                    "
                            "		SELECT                                                                    "
                            "			1                                                                       "
                            "		FROM                                                                      "
                            "			t_thinkauth_user_permission AS a                                        "
                            "			LEFT JOIN t_thinkauth_user AS b ON a.user_id = b.id                     "
                            "			LEFT JOIN t_thinkauth_permission AS c ON a.permission_id = c.id         "
                            "		WHERE                                                                     "
                            "			b.id = %s                                                         "
                            "			AND c.id = %s                                              "
                            "			                                                        "
                            "			)                                                                       "
                            "	OR EXISTS (                                                                 "
                            "		SELECT                                                                    "
                            "			1                                                                       "
                            "		FROM                                                                      "
                            "			t_thinkauth_group_permission AS a                                       "
                            "			LEFT JOIN t_thinkauth_group AS b ON a.group_id = b.id                   "
                            "			LEFT JOIN t_thinkauth_permission AS c ON a.permission_id = c.id         "
                            "		WHERE                                                                     "
                            "			c.id = %s                                                  "
                            "			                                                        "
                            "			AND b.id IN (                                                           "
                            "				SELECT                                                                "
                            "					d.group_id                                                          "
                            "				FROM                                                                  "
                            "					t_thinkauth_user_group AS d                                         "
                            "					LEFT JOIN t_thinkauth_user AS e on d.user_id = e.id                 "
                            "				WHERE                                                                 "
                            "					e.id = %s                                                     "
                            "			)                                                                       "
                            "	)                                                                           ",
                            (nUID, nPID, nPID, nUID))

                        rows = await cur.fetchall()
                        if rows is None or len(rows) <= 0:
                            return False

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return False
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return False

    @classmethod
    async def group_has_permission(cls, nGID, nPID):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute(
                            "SELECT                                                              "
                            "	1                                                                  "
                            "FROM                                                                "
                            "	t_thinkauth_group_permission AS a                                  "
                            "	LEFT JOIN t_thinkauth_group AS b ON a.group_id = b.id              "
                            "	LEFT JOIN t_thinkauth_permission AS c ON a.permission_id = c.id    "
                            "WHERE                                                               "
                            "	c.id = %s                                             "
                            "	AND b.id = %s                                                  ",
                            (nPID, nGID))

                        rows = await cur.fetchall()
                        if rows is None or len(rows) <= 0:
                            return False

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return False
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return False

    @classmethod
    async def grant_permission_to_user(cls, nPID, nUID):
        from pythinkutils.aio.tornado_auth.service.BaseUserService import BaseUserService

        bHasPermission = await cls.user_has_permission(nUID, nPID)
        if bHasPermission:
            return True

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_user_permission(user_id, permission_id) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (nUID, nPID))

                        await conn.commit()

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return False
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return False

    @classmethod
    async def grant_permissions_to_user(cls, lstPIDs, nUID):
        for nPID in lstPIDs:
            await cls.grant_permission_to_user(nPID, nUID)

        return True

    @classmethod
    async def grant_permission_to_group(cls, nPID, nGID):
        from pythinkutils.aio.tornado_auth.service.GroupService import GroupService

        bHasPermission = await cls.group_has_permission(nGID, nPID)
        if bHasPermission:
            return True

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_group_permission(group_id, permission_id) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (nGID, nPID))

                        await conn.commit()

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return False
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return False

    @classmethod
    async def grant_permissions_to_group(cls, lstPIDs, nGID):
        for nPID in lstPIDs:
            await cls.grant_permission_to_group(nPID, nGID)

        return True