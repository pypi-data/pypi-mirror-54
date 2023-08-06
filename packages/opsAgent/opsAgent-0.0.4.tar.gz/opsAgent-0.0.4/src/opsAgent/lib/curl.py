#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random
from urllib import parse

import pycurl
from opsAgent.lib.logger import LoggerHelper


class BufferIO(object):
    """
    buffer io
    """

    def __init__(self):
        self.contents = b''

    def body_callback(self, buf):
        self.contents += buf


def curl(url, header=None, data=None, gzip=False, method='GET'):
    """
    执行curl模拟请求, 并返回访问结果
    :param url: 访问地址
    :param header: 请求头
    :param data: 请求体
    :param gzip: 压缩
    :param method: 请求方式
    :return: 访问数据
    """
    log = LoggerHelper()

    http_header = []
    http_contents = b''

    if header:
        http_header.extend(header)

    c = pycurl.Curl()
    buffer = BufferIO()
    c.setopt(pycurl.WRITEFUNCTION, buffer.body_callback)

    if gzip:
        c.setopt(pycurl.ENCODING, 'gzip')  # 默认不启用压缩

    c.setopt(pycurl.URL, url)
    c.setopt(c.HTTPHEADER, http_header)
    c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 连接超时时间10s
    c.setopt(pycurl.TIMEOUT, 10)  # 定义请求超时时间10s
    c.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条
    c.setopt(pycurl.MAXREDIRS, 1)  # 指定HTTP重定向的最大数为1
    c.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 0)  # 设置保存DNS信息的时间为0秒
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)

    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    ]

    # 设置随机ua
    c.setopt(pycurl.USERAGENT, ua_list[random.randint(0, len(ua_list) - 1)])

    if method == 'POST':
        c.setopt(pycurl.POSTFIELDS, parse.urlencode(data))

    try:
        c.perform()

        # CONTENT_TYPE 处理，只发送响应内容是text类型的响应内容到服务端；
        # 响应内容包含: ["application", "image", "audio", "video", "drawing", "message", "java"] 响应内容直接移除
        content_type = c.getinfo(pycurl.CONTENT_TYPE)
        if 'text' in content_type:
            http_contents = buffer.contents

    except Exception as e:
        log.error_logger.log(logging.ERROR,
                             "curl return fail {e}".format(e=str(e)))
    return {
        # 返回HTTP状态码
        "http_status_code": c.getinfo(pycurl.HTTP_CODE) or 0,
        # 下载数据包的大小
        "http_size_download": c.getinfo(pycurl.SIZE_DOWNLOAD) or 0,
        # DNS解析所消耗的时间
        "http_name_lookup_time": c.getinfo(c.NAMELOOKUP_TIME) or 0,
        # 建立连接所消耗的时间
        "http_connect_time": c.getinfo(c.CONNECT_TIME) or 0,
        # 从建立连接到准备传输所消耗的时间
        "http_pretransfer_time": c.getinfo(c.PRETRANSFER_TIME) or 0,
        # 从建立连接到传输开始消耗的时间
        "http_start_transfer_time": c.getinfo(c.STARTTRANSFER_TIME) or 0,
        # 传输结束所消耗的总时间
        "http_total_time": c.getinfo(c.TOTAL_TIME) or 0,
        # 平均下载速度
        "http_speed_download": c.getinfo(c.SPEED_DOWNLOAD) or 0,
        # 返回响应内容
        "http_contents": http_contents
    }
