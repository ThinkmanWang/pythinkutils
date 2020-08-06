# -*- coding: UTF-8 -*-

import sys
import os
import pymysql as mysql
import threading
import psycopg2

from psycopg2.extras import DictCursor
from psycopg2.pool import ThreadedConnectionPool

from pythinkutils.config.Config import ThinkConfig

class ThinkPG:
    g_lock = threading.Lock()
    g_dictConnPool = {}

    @classmethod
    def get_conn_pool_ex(cls, szGroup="postgresql"):
        return cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                      , port=int(ThinkConfig.get_default_config().get(szGroup, "port"))
                      , user=ThinkConfig.get_default_config().get(szGroup, "user")
                      , password=ThinkConfig.get_default_config().get(szGroup, "password")
                      , db=ThinkConfig.get_default_config().get(szGroup, "db")
                      , mincached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections") / 2)
                      , maxcached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get(szGroup, "maxconnections"))
                      , charset="utf8"
                      , use_unicode=True)

    @classmethod
    def get_conn_pool(cls
                      , host=ThinkConfig.get_default_config().get("postgresql", "host")
                      , port=int(ThinkConfig.get_default_config().get("postgresql", "port"))
                      , user=ThinkConfig.get_default_config().get("postgresql", "user")
                      , password=ThinkConfig.get_default_config().get("postgresql", "password")
                      , db=ThinkConfig.get_default_config().get("postgresql", "db")
                      , mincached = int(ThinkConfig.get_default_config().get_int("postgresql", "maxconnections") / 2)
                      , maxcached = int(ThinkConfig.get_default_config().get_int("postgresql", "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get("postgresql", "maxconnections"))
                      , charset = "utf8"
                      , use_unicode = True):

        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            with cls.g_lock:
                if cls.g_dictConnPool.get(szHostPortDb) is None:


                    conn_pool = ThreadedConnectionPool(minconn=mincached
                                                       , maxconn=maxcached
                                                       , host=host
                                                       , database=db
                                                       , user=user
                                                       , password=password
                                                       , port=port)

                    cls.g_dictConnPool[szHostPortDb] = conn_pool


        return cls.g_dictConnPool.get(szHostPortDb)

# def main():
#
#     conn = ThinkPG.get_conn_pool_ex().getconn()
#     cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     # cur.execute("""SELECT count(1) as cnt from t_test_col """)
#     # rows = cur.fetchall()
#     # print(rows)
#
#     cur.execute("INSERT INTO t_test_col(id, name, score) VALUES (%s, %s, %s)", (1024000, "Thinkman Wang", 99))
#     conn.commit()
#
# if __name__ == '__main__':
#     main()