#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import requests

from requests import Request, Session
from requests.adapters import HTTPAdapter


class UrlHandle(object):

    def __init__(self, url, method="GET", headers=None, data=None,
                 cookies=None, allow_redirects=True, timeout=60, stream=None,
                 verify=False, proxies=None, cert=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.cookies = cookies
        self.allow_redirects = allow_redirects
        self.timeout = timeout
        self.stream = stream
        self.verify = verify
        self.proxies = proxies
        self.cert = cert
        self.result = {
            "data": None,
            "msg": '',
            "code": 0
        }

    def request(self):
        s = Session()

        s.mount('http://', HTTPAdapter(max_retries=2))  # 超时重试2次
        s.mount('https://', HTTPAdapter(max_retries=2))

        req = Request(
            self.method,
            self.url,
            data=self.data,
            headers=self.headers,
            cookies=self.cookies,
        )

        prepped = s.prepare_request(req)

        try:
            resp = s.send(
                prepped,
                stream=self.stream,
                verify=self.verify,
                proxies=self.proxies,
                cert=self.cert,
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
            )

        except requests.exceptions.ConnectTimeout:
            self.result["msg"] = "Network Connection Timeout"
            self.result["code"] = -1
            return self.result
        except requests.exceptions.ConnectionError:
            self.result["msg"] = "Network Connection Error"
            self.result["code"] = -2
            return self.result

        try:
            self.result["msg"] = resp.raise_for_status()
        except requests.exceptions.HTTPError:
            self.result["msg"] = "HTTP returns the error status code"
            self.result["code"] = resp.status_code

        resp.encoding = 'utf-8'
        self.result["code"] = resp.status_code
        self.result["data"] = resp.json()
        return self.result
