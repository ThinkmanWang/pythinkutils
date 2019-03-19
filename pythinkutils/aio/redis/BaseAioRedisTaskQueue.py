# -*- coding: UTF-8 -*-

import sys
import os
import asyncio
from abc import *

from thinkutils.log.log import g_logger
from thinkutils.common_utils.StringUtils import *

class BaseAioRedisTaskQueue(object):
    __metaclass__ = ABCMeta

    def __init__(self, queueName = "task_queue_default", size=1):
        self.m_szQueueName = queueName
        self.m_bStarted = False
        self._coroutine = []
        self.m_nSize = size


    def start(self):
        if self.m_bStarted:
            return

        for i in range(self.m_nSize):
            asyncio.gather(self.on_start())

        self.m_bStarted = True

    async def on_start(self):
        while True:
            try:
                from aiothinkutils.redis.ThinkAioRedisPool import ThinkAioRedisPool
                conn_pool = await ThinkAioRedisPool.get_default_conn_pool()
                with await conn_pool as conn:
                    szRet = await conn.execute('LPOP', self.m_szQueueName)
                    if bytes == type(szRet):
                        szRet = szRet.decode(encoding='utf-8')

                    if is_empty_string(szRet):
                        await asyncio.sleep(2)
                        continue

                    await self.on_task(szRet)
            except Exception as e:
                pass

    @abstractmethod
    async def on_task(self, szMsg):
        pass

    @classmethod
    async def put_real(cls, szQueueName = "task_queue_default", szMsg = ""):
        try:
            from aiothinkutils.redis.ThinkAioRedisPool import ThinkAioRedisPool
            conn_pool = await ThinkAioRedisPool.get_default_conn_pool()
            with await conn_pool as conn:
                await conn.execute("RPUSH", szQueueName, szMsg)
        except Exception as e:
            pass

    @classmethod
    async def put(cls, szQueueName = "task_queue_default", szMsg = "", nowait = False):
        if nowait:
            asyncio.gather(cls.put_real(szQueueName, szMsg))
        else:
            await cls.put_real(szQueueName, szMsg)

    @classmethod
    def put_nowait(cls, szQueueName = "task_queue_default", szMsg = ""):
        asyncio.gather(cls.put(szQueueName, szMsg, True))