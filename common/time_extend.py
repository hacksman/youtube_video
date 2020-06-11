# -*- encoding: utf-8 -*-
# @Time :2020/4/15 7:29 PM

from loguru import logger
import arrow


class TimeExtend:

    @classmethod
    def datetime_to_human(cls, t=None, fmt="%Y-%m-%d %H:%M:%S", only_date=False):
        t = arrow.now() if not t else t
        fmt = fmt if not only_date else "%Y-%m-%d"
        return t.strftime(fmt)

    @classmethod
    def timestamp_to_human(cls, t=None, fmt="%Y-%m-%d %H:%M:%S"):
        t = arrow.now().timestamp if not t else t
        time_now = arrow.get(t).shift(hours=+8).strftime(fmt)
        return time_now

    @classmethod
    def human_date_to_timestamp(cls, t=None):
        time_stamp = arrow.get(t).shift(hours=-8).timestamp
        return time_stamp

    @classmethod
    def human_date_yesterday_start(cls, floor="day"):
        time_stamp = arrow.now().shift(days=-1).floor(floor).timestamp
        return cls.timestamp_to_human(time_stamp)

    @classmethod
    def human_date_yesterday_end(cls, floor="day"):
        time_stamp = arrow.now().shift(days=-1).ceil(floor).timestamp
        return cls.timestamp_to_human(time_stamp)


if __name__ == '__main__':
    logger.info(TimeExtend.datetime_to_human())
    logger.info(TimeExtend.timestamp_to_human())
    logger.info(TimeExtend.human_date_to_timestamp("2020-04-27 19:10:07"))
    logger.info(TimeExtend.human_date_yesterday_start(floor="day"))
    logger.info(TimeExtend.human_date_yesterday_end(floor="day"))
    logger.info(TimeExtend.timestamp_to_human(fmt="%Y%m%d"))
