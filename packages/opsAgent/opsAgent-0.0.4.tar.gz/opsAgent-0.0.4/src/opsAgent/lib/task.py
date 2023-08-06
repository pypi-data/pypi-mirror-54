# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

from opsAgent.lib.auth import get_http_headers
from opsAgent.lib.curl import curl
from opsAgent.lib.http import UrlHandle
from opsAgent.lib.logger import LoggerHelper
from opsAgent.lib.scheduler import scheduler
from opsAgent.lib.vars import GlobalVars


def fetch_task_list():
    """
    从后端获取监控任务列表，并与本地监控任务列表比对，移除无效任务
    :return:
    """
    var = GlobalVars()
    log = LoggerHelper()

    headers = get_http_headers(var, var.web_task_api)

    # 获取监控任务列表
    resp = UrlHandle(url=var.web_task_api, method='GET', headers=headers)
    result = resp.request()

    if result["code"] == 200:
        # 服务端返回的数据
        data = result["data"]["data"]

        # 存储服务端返回的任务信息
        task_list = {}

        # 本地任务列表
        local_task_list = var["task_list"]

        # 循环监控任务列表;
        for item in data:
            id = item["id"]
            name = item["name"]
            url = item["url"]
            monitor_type = item["monitor_type"]
            monitor_interval = item["monitor_interval"]
            http_header = item["http_header"]
            post_requst_body = item["post_requst_body"]
            web_worker = item["web_worker"]
            enable = item["enable"]

            if not enable:  # 如果任务已经禁用，直接跳过
                continue

            if var["ID"] not in web_worker:
                continue

            # 将分配的任务存放task_list中
            task_list[id] = {
                "name": name,
                "url": url,
                "monitor_type": monitor_type,
                "monitor_interval": monitor_interval,
                "http_header": http_header,
                "post_requst_body": post_requst_body,
                "enable": enable
            }

            # log.access_logger.info("fetch new task, name: {name} url: {url}".format(name=name, url=url))

            if id not in local_task_list.keys():  # 如果服务端返回的任务信息不在本地任务列表中
                local_task_list[id] = item
                local_task_list[id]["has_change"] = False  # 标记任务变化状态，初始化为False
                log.access_logger.info("insert new task: %s." % name)
            else:  # 如果服务端返回的信息在本地任务列表中，则对比任务信息，如果发生了变化则更新任务状态
                local_task = local_task_list[id]

                # 如果任务已经标记了发生改变，那么就不用对比本地和服务端信息
                if not local_task["has_change"]:
                    # 对比服务端和本地的任务信息
                    if local_task["name"] != name:
                        local_task["name"] = name
                        local_task["has_change"] = True

                    if local_task["url"] != url:
                        local_task["url"] = url
                        local_task["has_change"] = True

                    if local_task["monitor_type"] != monitor_type:
                        local_task["monitor_type"] = monitor_type
                        local_task["has_change"] = True

                    if local_task["monitor_interval"] != monitor_interval:
                        local_task["monitor_interval"] = monitor_interval
                        local_task["has_change"] = True

                    if local_task["http_header"] != http_header:
                        local_task["http_header"] = http_header
                        local_task["has_change"] = True

                    if local_task["post_requst_body"] != post_requst_body:
                        local_task["post_requst_body"] = post_requst_body
                        local_task["has_change"] = True

                    if local_task["enable"] != enable:
                        local_task["enable"] = enable
                        local_task["has_change"] = True

                    # 如果任务发生了变化，记录到日志
                    if local_task["has_change"]:
                        log.access_logger.info("task: %s has changed." % name)

        # 对比服务端返回的任务列表和本地的任务列表，移除禁用或者不存在的任务信息
        invalid_task_list = []  # 无效的任务列表

        for item in local_task_list.keys():
            if item not in task_list:  # 如果本地的任务不在服务端返回的任务列表中，就加入到无效的列表中
                invalid_task_list.append(item)

        # 从本地任务列表中移除无效的任务
        for item in invalid_task_list:
            local_task_list.pop(item)
            log.access_logger.log(logging.INFO, "remove invalid task: %s." % local_task_list[item]["name"])

        # 将更新之后的任务信息保存到全局变量中
        var["task_list"] = local_task_list
    else:
        log.error_logger.error("failed to fetch task list, msg:%s, code: %s." % (result["msg"], result["code"]))


def build_cron_task():
    """
    根据本地的任务列表生成定时任务
    :return:
    """
    var = GlobalVars()
    log = LoggerHelper()

    local_task_list = var["task_list"]

    # 创建任务
    for item in local_task_list.keys():
        local_task = local_task_list[item]
        task_name = 'task-%s' % local_task["id"]  # 监控任务名称
        task_interval = int(local_task["monitor_interval"])  # 监控频率

        # 如果任务已经存在而且任务状态发生了变化, 就删除这个任务
        if scheduler.get_job(task_name):
            if local_task["has_change"]:
                scheduler.remove_job(task_name)
                log.access_logger.log(logging.INFO, "job has change, remove job: %s." % task_name)

                # 将任务状态重置为false
                local_task["has_change"] = False
            else:
                continue  # 如果任务已经存在，而且没有发送变化，直接跳过
        else:  # 如果任务不存在，那么就生成新任务
            task_interval_time_list = [1, 5, 10, 15, 30, 60]
            if task_interval < len(task_interval_time_list):  # 确保监控任务间隔处于时间列表中
                scheduler.add_job(
                    func=web_task_executor,
                    args=(local_task,),
                    trigger='interval',
                    minutes=task_interval_time_list[task_interval],
                    id=task_name
                )
                log.access_logger.log(logging.INFO, "add new job: %s" % task_name)
            else:
                log.error_logger.error("job %s unsupported intervals time." % task_name)

    # 移除失效的任务, 对比本地任务和当前正在运行的任务，移除本地任务列表中不存在的任务
    for item in scheduler.get_jobs():

        if str(item.id).startswith('task-'):
            task_name = item.id
            task_id = int(str(item.id).split('task-')[1])

            if task_id not in local_task_list.keys():
                scheduler.remove_job(task_name)
                log.access_logger.info("remove invalid job: %s." % task_name)


def web_task_executor(task):
    """
    执行web监控任务，并上报监控数据
    :param task: web任务信息
    :return:
    """
    var = GlobalVars()
    log = LoggerHelper()

    header = []
    data = {}
    time_now = int(time.time())

    # 处理请求头
    for item in task["http_header"].split('\n'):
        header.append(item)

    # 处理请求体
    for item in task["post_requst_body"].split('\n'):
        if item.strip():
            key = item.split(':')[0]
            value = item.split(':')[1]
            data[key] = value

    monitor_type = task["monitor_type"]
    http_method_list = ['GET', 'POST', 'HEAD']

    if monitor_type < len(http_method_list):
        method = http_method_list[monitor_type]
    else:
        log.error_logger.info("task: %s invalid monitor_type" % task["name"])
        return

    if not task["url"].startswith("http"):  # 如果监控url不是一个有效的url链接，直接返回
        log.error_logger.error("invalid url address %s" % task["name"])
        return

    # 模拟访问监控url，获取访问结果
    resp = curl(url=task["url"], header=header, data=data, method=method)

    monitor_data = {
        "id": task['id'],
        "url": task["url"],
        "create_at": time_now,
        "http_status_code": resp["http_status_code"],
        "http_size_download": resp["http_size_download"],
        "http_name_lookup_time": resp["http_name_lookup_time"],
        "http_connect_time": resp["http_connect_time"],
        "http_pretransfer_time": resp["http_pretransfer_time"],
        "http_start_transfer_time": resp["http_start_transfer_time"],
        "http_total_time": resp["http_total_time"],
        "http_speed_download": resp["http_speed_download"],
        "http_contents": resp["http_contents"]
    }

    # 监控数据上报到服务端
    resp = UrlHandle(var.web_task_report_api, method='POST', data=monitor_data,
                     headers=get_http_headers(var, var.web_task_report_api))
    result = resp.request()

    if result["code"] == 200:
        log.access_logger.info("successful data upload, task: %s" % task["name"])
    else:  # 上传失败
        log.error_logger.log(logging.ERROR, "failure to upload data, task: %s, msg: %s" % (task["name"], result["msg"]))
