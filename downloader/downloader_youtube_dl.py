# coding: utf-8
# @Time : 2020/6/1 2:15 PM

import os
import redis
import json
import time
import click
import youtube_dl
import sys

sys.path.append('../')
sys.path.append('../..')
sys.path.append('../../..')

from pathlib import Path
from config.redis_conf import RedisConf

from loguru import logger


class DownloaderYoutubeDl(object):

    def __init__(self, save_video_base_path, use_proxy):

        self.save_video_base_path = save_video_base_path

        self.video_info_redis = redis.StrictRedis(host=RedisConf.REDIS_HOST,
                                                  port=RedisConf.REDIS_PORT,
                                                  db=RedisConf.REDIS_DB,
                                                  decode_responses=True)

        self.ydl_opts = {"proxy": "socks5://127.0.0.1:1081"} if use_proxy else {}

    def download_video(self, video_info):
        video_url = video_info["video_share_url"]
        path_dir = Path(self.save_video_base_path)
        if not path_dir.exists():
            os.makedirs(path_dir)
        self.ydl_opts.update({"outtmpl": f"{self.save_video_base_path}/%(id)s.%(ext)s"})
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([video_url])
                return True
            except BaseException as e:
                logger.error(f"『{video_url}』download error happened:")
                logger.error(e)
                return False

    def run(self):
        while True:
            for video_key in self.video_info_redis.scan_iter(f"*YOUTUBE*"):
                # redis key 为空的情况
                video_info = self.video_info_redis.get(video_key)
                video_info = json.loads(video_info, encoding="utf-8")

                video_id = video_info["video_id"]
                business = video_info["business"]
                dl_cnt = video_info.get("dl_cnt", 0)

                if dl_cnt > 3:
                    logger.warning(f"「{business}」【{video_id}】视频下载超过 3 次...不再下载")
                    continue

                download_video_succeed = self.download_video(video_info)

                video_info['dl_cnt'] = dl_cnt + 1
                if download_video_succeed:
                    # 基础字段

                    self.video_info_redis.delete(video_key)
                    logger.info(f"下载「{business}」【{video_id}】数据成功...")
                else:
                    self.video_info_redis.getset(video_key, json.dumps(video_info))
                    logger.error(f"下载「{business}」【{video_id}】数据失败...")
                    continue
                time.sleep(1)


@click.command()
@click.option("--save_video_base_path",
              type=str,
              default=".\\" if os.name == "nt" else "./",
              help="下载文件的根目录")
@click.option("--use_proxy",
              type=bool,
              default=False,
              help="使用代理， 默认为False")
def main(save_video_base_path, use_proxy):
    d = DownloaderYoutubeDl(save_video_base_path, use_proxy)
    d.run()


if __name__ == '__main__':
    main()
