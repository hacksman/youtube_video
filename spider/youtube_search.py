# coding: utf-8
# @Time : 2020/6/11 9:31 AM

import sys
sys.path.append("../")
sys.path.append("../..")

import click
import time
import arrow
from spider.spider_base import SpiderBase

from common.fetch import fetch
from common.time_extend import TimeExtend

from spider.url import UrlYoutube

from loguru import logger


class YoutubeSearch(SpiderBase):

    def __init__(self):
        super().__init__()
        self.app_key = 'YOUR APP KEY'  # jizai

    def grab_search(self, search_word, page_token=None):
        headers = {"user-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"}
        search_video_url = UrlYoutube.video_search(self.app_key, search_word, page_token)

        # resp = fetch(search_video_url, headers=headers, use_proxy=True)
        resp = fetch(search_video_url, headers=headers, use_proxy=False)

        resp_json = resp.json()

        if not page_token:
            logger.info(f"『{search_word}』总共有【{resp_json['pageInfo']['totalResults']}】条数据...")

        if not resp_json["items"]:
            return None

        results = []
        for item in resp_json["items"]:
            try:
                logger.info(f"当前爬取\t{item['snippet']['publishedAt']}\t的数据")
                video_id = item["id"].get("videoId")
                if not video_id:
                    logger.warning(f"爬取到一条非法视频:{item}")
                    continue
                # video_info = resp_video.json()["items"][0]
                video_info = dict()
                video_info["business"] = "Youtube"
                # 信息字段 - 用户信息
                snippet = item["snippet"]
                video_info["user_name"] = snippet["channelTitle"]
                video_info["user_id"] = snippet["channelId"]
                # 信息字段 - 视频信息
                video_info["video_id"] = video_id
                video_info["video_title"] = snippet["title"]
                video_info["video_desc"] = snippet["description"]
                video_info["video_share_url"] = f"https://www.youtube.com/watch?v={video_id}"
                video_info["video_create_time"] = TimeExtend.timestamp_to_human(arrow.get(snippet["publishedAt"]).timestamp)

                results.append(video_info)
            except BaseException as e:
                logger.error("some error happened:")
                logger.error(e)
                continue

        self.send_redis(results)

        next_page_token = resp_json.get("nextPageToken")

        return next_page_token

    def run(self, word):

        page = 0
        next_page_token = None

        while True:
            page += 1
            logger.info(f"爬取关键词『{word}』的第『{page}』页...")
            next_page_token = self.grab_search(word, next_page_token)
            if not next_page_token:
                logger.info(f"爬取关键词『{word}』的第『{page}』页...")
                break
            time.sleep(3)


@click.command()
@click.option("--word",
              type=str,
              default="hello world",
              help="检索词")
def main(word):
    d = YoutubeSearch()
    d.run(word)


if __name__ == '__main__':
    main()
