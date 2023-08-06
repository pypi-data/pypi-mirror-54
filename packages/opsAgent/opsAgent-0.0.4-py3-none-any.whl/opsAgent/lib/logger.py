# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-


import logging

from opsAgent.lib.path import log_file_path
from logging.handlers import RotatingFileHandler


class LoggerHelper(object):
    _i = None

    def __new__(cls, *args, **kwargs):
        if cls._i:
            return cls._i
        else:
            obj = object.__new__(cls)
            cls._i = obj
            return cls._i

    def __init__(self):

        log_path = log_file_path()

        error_log_file = RotatingFileHandler(filename='%s/error.log' % log_path, maxBytes=10485760, backupCount=10,
                                             encoding='utf-8')
        error_log_fmt = logging.Formatter(fmt="%(asctime)s %(filename)s %(funcName)s %(name)s %(message)s")
        error_log_file.setFormatter(error_log_fmt)
        error_logger = logging.Logger('ERROR', level=logging.ERROR)
        error_logger.addHandler(error_log_file)
        self.error_logger = error_logger

        access_log_file = RotatingFileHandler(filename='%s/access.log' % log_path, maxBytes=10485760, backupCount=10,
                                              encoding='utf-8')
        access_log_fmt = logging.Formatter(fmt="%(asctime)s %(name)s %(message)s")
        access_log_file.setFormatter(access_log_fmt)
        access_logger = logging.Logger('INFO', level=logging.INFO)
        access_logger.addHandler(access_log_file)
        self.access_logger = access_logger
