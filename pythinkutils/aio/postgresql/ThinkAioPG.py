# -*- coding: utf-8 -*-

import sys
import os

import asyncio
import aiopg
import aiorwlock
import pymysql
import psycopg2

from psycopg2.extras import DictCursor

from pythinkutils.config.Config import *
from pythinkutils.common.log import g_logger

class ThinkAioPG(object):
    g_dictConnPool = {}
    g_rwlock = aiorwlock.RWLock()

    @classmethod
    async def get_conn_pool_ex(cls, szGroup="postgresql"):
        ret = await cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                                      , port=int(ThinkConfig.get_default_config().get(szGroup, "port"))
                                      , user=ThinkConfig.get_default_config().get(szGroup, "user")
                                      , password=ThinkConfig.get_default_config().get(szGroup, "password")
                                      , db=ThinkConfig.get_default_config().get(szGroup, "db")
                                      , mincached=int(
                ThinkConfig.get_default_config().get_int(szGroup, "maxconnections") / 2)
                                      ,
                                      maxcached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections"))
                                      , maxconnections=int(
                ThinkConfig.get_default_config().get(szGroup, "maxconnections"))
                                      , charset="utf8"
                                      , use_unicode=True)

        return ret

    @classmethod
    async def get_conn_pool(cls
                            , host=ThinkConfig.get_default_config().get("postgresql", "host")
                            , port=int(ThinkConfig.get_default_config().get("postgresql", "port"))
                            , user=ThinkConfig.get_default_config().get("postgresql", "user")
                            , password=ThinkConfig.get_default_config().get("postgresql", "password")
                            , db=ThinkConfig.get_default_config().get("postgresql", "db")
                            , mincached=int(ThinkConfig.get_default_config().get_int("postgresql", "maxconnections") / 2)
                            , maxcached=int(ThinkConfig.get_default_config().get_int("postgresql", "maxconnections"))
                            , maxconnections=int(ThinkConfig.get_default_config().get("mysql", "maxconnections"))
                            , charset="utf8"
                            , use_unicode=True):
        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            async with cls.g_rwlock.writer:
                if cls.g_dictConnPool.get(szHostPortDb) is None:
                    dsn = 'dbname={} user={} password={} host={} port={}'.format(db, user, password, host, port)
                    connPool = await aiopg.create_pool(
                        dsn = dsn
                        , minsize=mincached
                        , maxsize=maxcached)

                    cls.g_dictConnPool[szHostPortDb] = connPool

        return cls.g_dictConnPool.get(szHostPortDb)


# async def main():
#     with await (await ThinkAioPG.get_conn_pool_ex()) as conn:
#         cur = await conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#         await cur.execute("SELECT 1 as fxxk")
#         ret = []
#         async for row in cur:
#             ret.append(dict(row))
#
#         print(ret)
#
#         await cur.execute("INSERT INTO t_test_col(id, name, score) VALUES (%s, %s, %s)", (1024001, "Thinkman Wang", 99))
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())