# coding: utf-8
# @Time : 2020/6/11 9:59 AM

import redis
import json

from loguru import logger
from typing import (NoReturn, List)
from config.redis_conf import RedisConf


class SpiderBase:

    @property
    def video_info_redis(self):
        return redis.StrictRedis(host=RedisConf.REDIS_HOST,
                                 port=RedisConf.REDIS_PORT,
                                 db=RedisConf.REDIS_DB,
                                 decode_responses=True)

    def send_redis(self, search_results: List) -> NoReturn:
        for result in search_results:
            video_id = result["video_id"]
            try:
                redis_key = ":".join(("YOUTUBE", "VIDEO", video_id))
                result = json.dumps(result)
                self.video_info_redis.set(redis_key, result)
            except BaseException as e:
                logger.error(f"[{video_id}] 发送信息至 redis 错误：")
                logger.error(e)
                logger.error("result>>>>>>")
                logger.error(result)
                continue

