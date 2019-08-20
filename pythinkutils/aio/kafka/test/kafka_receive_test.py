# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
from pythinkutils.aio.kafka.ThinkAioKafkaConsumer import ThinkAioKafkaConsumer
from pythinkutils.config.Config import g_config
from pythinkutils.aio.common.aiolog import g_aio_logger

class TestConsumer(ThinkAioKafkaConsumer):

    def __init__(self, szHost, szTopic, szGroup):
        super().__init__(szHost, szTopic, szGroup)

    async def on_msg(self, msg):
        # await asyncio.sleep(5)
        # random.randint
        # print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
        szMsg = str(msg.value, "utf-8")
        g_aio_logger.info(szMsg)


def main():
    loop = asyncio.get_event_loop()

    myConsumer = TestConsumer(g_config.get("kafka", "host"), g_config.get("kafka", "topic"), "myGroup")
    myConsumer.start()

    loop.run_forever()

if __name__ == '__main__':
    main()
