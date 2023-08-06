#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GlobalVars(object):
    """存储全局变量"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not GlobalVars.__instance:
            obj = object.__new__(cls)
            GlobalVars.__instance = obj
        return GlobalVars.__instance

    @property
    def register_api(self):
        """
        :return: 服务端认证接口地址
        """
        return 'http://{ip}:{port}/api/ops/agent' \
            .format(ip=self.__dict__["SERVER_HOST"],
                    port=self.__dict__["SERVER_PORT"])

    @property
    def web_task_api(self):
        """
        :return: 获取任务列表API地址
        """
        return 'http://{ip}:{port}/api/ops/agent/web/list' \
            .format(ip=self.__dict__["SERVER_HOST"],
                    port=self.__dict__["SERVER_PORT"])

    @property
    def web_task_report_api(self):
        """
        :return: 汇报监控数据API地址
        """
        return 'http://{ip}:{port}/api/ops/agent/web/report' \
            .format(ip=self.__dict__["SERVER_HOST"],
                    port=self.__dict__["SERVER_PORT"])

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        self.__dict__.pop(key)
