# -*- encoding: utf-8 -*-
# @Time :2020/4/14 2:21 PM


import random

from loguru import logger
from resources import USER_AGENT

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from retrying import retry

DEFALUT_REQ_TIMEOUT = 5
MAX_RETRY_REQ_TIMES = 3
RETRY_RANDON_MIN_WAIT = 1000  # ms
RETRY_RANDON_MAX_WAIT = 5000  # ms


def get_proxy(url):
    # proxy_url = "http://0.0.0.0:9600/proxy?host=gsxt.gdgs.gov.cn&tag=yizhou"
    # proxies_rsp = requests.get(proxy_url)
    # if proxies_rsp.json().get("status") == "fail":
    #     return {}
    # proxies = {"http": proxies_rsp.json()["proxy"], "https": proxies_rsp.json()["proxy"].replace("http", "https")}
    proxies = {"http": "socks5h://127.0.0.1:1081", "https": "socks5h://127.0.0.1:1081"}
    return proxies


def need_retry(exception):
    result = isinstance(exception, (requests.ConnectionError, requests.ReadTimeout))
    if result:
        logger.warning(f"Exception[{type(exception)}]\toccurred retrying...")
    return result


def fetch(url: str, use_proxy: bool = False, **kwargs):
    @retry(stop_max_attempt_number=MAX_RETRY_REQ_TIMES, wait_random_min=RETRY_RANDON_MIN_WAIT,
           wait_random_max=RETRY_RANDON_MAX_WAIT, retry_on_exception=need_retry)
    def _fetch(url: str, **kwargs):
        kwargs.update({"verify": False})
        kwargs.update({"timeout": kwargs.get("timeout") or DEFALUT_REQ_TIMEOUT})
        if use_proxy:
            proxy = get_proxy(url)
            if not proxy:
                raise requests.ConnectionError(f"request get proxy failed")
            kwargs.update({"proxies": proxy})
        # 没有传入 headers 的情况下，默认带上一个 PC 端请求头 user-agent
        if not kwargs.get("headers"):
            kwargs.update({"headers": {"user-agent": random.choice(USER_AGENT["firefox"])}})
        if kwargs.get("method") in ["post", "POST"]:
            kwargs.pop("method", None)
            response = requests.post(url, **kwargs)
        else:
            response = requests.get(url, **kwargs)
        if response.status_code != 200:
            raise requests.ConnectionError(f"request status code should be 200! but got {response.status_code}")
        return response

    try:
        result = _fetch(url, **kwargs)
        return result
    except (requests.ConnectionError, requests.ReadTimeout):
        return None


if __name__ == '__main__':
    resp = fetch("http://www.cip.cc", use_proxy=True)

    logger.info(resp.text)

    # new_resp = fetch("https://www.ixigua.com/i6811020253397516812", cookies=resp.cookies)
    #
    # logger.info(new_resp.text)

