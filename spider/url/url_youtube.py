# -*- encoding: utf-8 -*-
# @Time :2020/5/19 9:58 AM

from loguru import logger

from furl import furl


class UrlYoutube:
    google_api_host_url = "https://www.googleapis.com"

    @classmethod
    def video_search(cls, app_key, search_word, page_token):
        # https://www.googleapis.com/youtube/v3/search?maxResults=25&q=surfing&key=[YOUR_API_KEY]
        dynamic_params = {'q': search_word,
                          'maxResults': 50,
                          'key': app_key,
                          "part": "snippet,id",
                          "pageToken": page_token}

        f_url = furl(cls.google_api_host_url).join('/youtube/v3/search').add(dynamic_params)
        return f_url.url


if __name__ == '__main__':
    logger.info(UrlYoutube.video_search("UC6FcYHEm7SO1jpu5TKjNXEA",
                                            "AIzaSyBOHd5b3ZYOntJBcM3sip8ydB9JwFs6Uck",
                                            # start_date="2020-05-13",
                                            # end_date="2020-05-20",
                                            page_token=None))
