# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import logging
import time

import opsAgent
from opsAgent.lib.auth import get_http_headers
from opsAgent.lib.http import UrlHandle
from opsAgent.lib.logger import LoggerHelper
from opsAgent.lib.vars import GlobalVars


def report_agent_status():
    """
    上报心跳信息
    """
    var = GlobalVars()
    headers = get_http_headers(var, var.register_api)
    data = {
        't': int(time.time()),
        "version": opsAgent.version
    }
    log = LoggerHelper()

    resp = UrlHandle(var.register_api, method='POST', data=data, headers=headers)
    result = resp.request()

    if result["code"] == 200:
        log.access_logger.log(logging.INFO, "successful reported agent status.")
    else:
        log.error_logger.error("failure to report agent status, msg:%s, code: %s." % (result["msg"], result["code"]))
