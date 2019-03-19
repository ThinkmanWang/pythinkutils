# -*- coding: UTF-8 -*-

import sys
import os

import aiomysql

from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class PermissionService(object):

    @classmethod
    async def create_permission(cls, szName, szDescription = "", nOwner = 10000001):
        dictPermission = await cls.select_permission(szName, nOwner)
        if dictPermission is not None:
            return dictPermission

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_permission(`permission_name`, owner, description) "
                                          "VALUES "
                                          "  (%s, %s, %s)"
                                          , (szName, nOwner, szDescription))

                        await conn.commit()

                        dictRet = await cls.select_permission(szName, nOwner)
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
    async def select_permission(cls, szName, nOwner = 10000001):
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
                                          "  AND owner = %s "
                                          "LIMIT 1 ", (szName, nOwner))

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
    async def user_has_permission(cls, szUser, szPermission, nOwner = 10000001):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT                                                                       "
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
                                          "			b.username = %s                                                         "
                                          "			AND c.permission_name = %s                                              "
                                          "			AND c.owner = %s                                                        "
                                          "			)                                                                       "
                                          "	OR EXISTS (                                                                 "
                                          "		SELECT                                                                    "
                                          "			1                                                                       "
                                          "		FROM                                                                      "
                                          "			t_thinkauth_group_permission AS a                                       "
                                          "			LEFT JOIN t_thinkauth_group AS b ON a.group_id = b.id                   "
                                          "			LEFT JOIN t_thinkauth_permission AS c ON a.permission_id = c.id         "
                                          "		WHERE                                                                     "
                                          "			c.permission_name = %s                                                  "
                                          "			AND c.owner = %s                                                        "
                                          "			AND b.id IN (                                                           "
                                          "				SELECT                                                                "
                                          "					d.group_id                                                          "
                                          "				FROM                                                                  "
                                          "					t_thinkauth_user_group AS d                                         "
                                          "					LEFT JOIN t_thinkauth_user AS e on d.user_id = e.id                 "
                                          "				WHERE                                                                 "
                                          "					e.username = %s                                                     "
                                          "			)                                                                       "
                                          "	)                                                                           ", (szUser, szPermission, nOwner, szPermission, nOwner, szUser))

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
    async def group_has_permission(cls, nGroupID, szPermission, nOwner = 10000001):
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
                                            "	c.permission_name = %s                                             "
                                            "	AND c.OWNER = %s                                                   "
                                            "	AND b.id = %s                                                  ", (szPermission, nOwner, nGroupID))

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
    async def grant_permission_to_user(cls, szPermission, szUser, nOwner = 10000001):
        from pythinkutils.aio.tornado_auth.service.BaseUserService import BaseUserService

        bHasPermission = await cls.user_has_permission(szUser, szPermission, nOwner)
        if bHasPermission:
            return True

        dictPermission = await cls.select_permission(szPermission, nOwner)
        if dictPermission is None:
            return False

        nUID = await BaseUserService.get_user_id(szUser)
        if nUID < 0:
            return False

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_user_permission(user_id, permission_id) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (nUID, dictPermission["id"]))

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
    async def grant_permissions_to_user(cls, lstPermission, szUser, nOwner = 10000001):
        for szPermission in lstPermission:
            await cls.grant_permission_to_user(szPermission, szUser, nOwner)

        return True

    @classmethod
    async def grant_permission_to_group(cls, szPermission, nGroupID, nOwner = 10000001):
        from pythinkutils.aio.tornado_auth.service.GroupService import GroupService

        bHasPermission = await cls.group_has_permission(nGroupID, szPermission, nOwner)
        if bHasPermission:
            return True

        dictPermission = await cls.select_permission(szPermission, nOwner)
        if dictPermission is None:
            return False

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_group_permission(group_id, permission_id) "
                                          "VALUES "
                                          "  (%s, %s)"
                                          , (nGroupID, dictPermission["id"]))

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
    async def grant_permissions_to_group(cls, lstPermission, nGroupID, nOwner = 10000001):
        for szPermission in lstPermission:
            await cls.grant_permission_to_user(szPermission, nGroupID, nOwner)

        return True

    # @classmethod
    # async def check_user_permission(cls, szUser, szPermission, nOwner = 10000001):
    #     pass
    #
    # @classmethod
    # async def check_user_permissions(cls, szUser, lstPermission, nOwner = 10000001):
    #     pass
    #
    # @classmethod
    # async def check_group_permission(cls, szGroup, szPermission, nOwner = 10000001):
    #     pass
    #
    # @classmethod
    # async def check_group_permissions(cls, szGroup, lstPermission, nOwner = 10000001):
    #     pass