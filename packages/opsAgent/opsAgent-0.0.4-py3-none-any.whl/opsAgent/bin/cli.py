#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import json
import argparse

from opsAgent.lib.scheduler import scheduler

from opsAgent.lib.vars import GlobalVars
from opsAgent.lib.logger import LoggerHelper

from opsAgent.config import settings
from opsAgent.lib.status import report_agent_status
from opsAgent.lib.task import fetch_task_list, build_cron_task


def run(config):
    var = GlobalVars()

    config_file = config if config else './config.json'

    if not os.path.exists(config_file):
        print("Error: Configuration file does not exist!")
        exit(126)

    # 读取配置文件
    try:
        with open(config_file, mode="r", encoding="utf-8") as f2:
            config_obj = json.load(f2)
    except Exception as e:
        print("Error: Illegal configuration file!", e)
        exit(127)

    # 将配置文件中的配置信息写入到类变量中
    for k, v in config_obj.items():
        var[k] = v

    # 检查配置文件必须配置的参数
    for item in ["SERVER_HOST", "SERVER_PORT", "ID", "TOKEN"]:
        if item not in var.__dict__.keys():
            print("Error: Missing configuration item: {item}!".format(item=item))
            exit(128)

    # DEBUG MODE
    debug_mode = var.__dict__.get("DEBUG", None)
    if debug_mode is not None:
        debug = debug_mode
    else:
        debug = settings.DEBUG

    if debug:
        debug_logger = logging.getLogger('apscheduler.executors.default')
        debug_logger.setLevel(logging.INFO)
        fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        h = logging.StreamHandler()
        h.setFormatter(fmt)
        debug_logger.addHandler(h)

    # 初始化变量
    var["task_list"] = {}

    log = LoggerHelper()
    log.access_logger.info("Initialization successful..")

    # 每1分钟, 向服务端上报监控端状态信息
    scheduler.add_job(
        func=report_agent_status,
        trigger='interval',
        minutes=1,
        id="report_agent_status_handler"
    )

    # 每1分钟, 获取监控任务列表
    scheduler.add_job(
        func=fetch_task_list,
        trigger='interval',
        minutes=1,
        id="fetch_task_list_handler"
    )

    # 每1分钟, 动态生成监控任务
    scheduler.add_job(
        func=build_cron_task,
        trigger='interval',
        minutes=1,
        id="build_cron_task_handler"
    )

    scheduler.start()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        dest="config",
        required=False,
        default="",
        help="Path To Configuration File"
    )

    args = parser.parse_args()
    run(args.config)
