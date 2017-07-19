# coding: utf-8

import logging
import os
from datetime import datetime


class Log(object):

    logger = None

    handler = None

    log_path = None

    @classmethod
    def path(cls, level):
        pwd = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.realpath(os.path.join(pwd, os.pardir))
        filename = 'info.log'
        if level == logging.INFO:
            filename = 'info.log'
        elif level == logging.ERROR:
            filename = 'err.log'
        elif level == logging.WARN:
            filename = 'warn.log'

        log_dir = os.path.join(root_path, 'data', 'logs', datetime.now().strftime('%Y%m%d%H'))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, filename)
        if not os.path.isfile(log_path):
            open(log_path, 'w').close()

        return log_path

    @classmethod
    def err(cls, msg):
        cls._init(logging.ERROR)
        return cls.logger.error(msg)

    @classmethod
    def info(cls, msg):
        cls._init(logging.INFO)
        return cls.logger.info(msg)

    @classmethod
    def warn(cls, msg):
        cls._init(logging.WARN)
        return cls.logger.warn(msg)

    @classmethod
    def debug(cls, msg):
        cls._init(logging.DEBUG)
        return cls.logger.debug(msg)

    @classmethod
    def _init(cls, level):
        log_path = cls.path(level)

        if not cls.logger:
            cls.logger = logging.getLogger()
        if cls.handler is None or cls.log_path != log_path:
            cls.log_path = log_path
            cls.handler = logging.FileHandler(log_path)

        # %(name)s %(filename)s %(levelname)s %(process)d
        fmt = "%(asctime)s %(pathname)s:%(lineno)d | %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S %a"
        formatter = logging.Formatter(fmt, datefmt)
        cls.handler.setFormatter(formatter)
        cls.handler.setLevel(level)
        cls.logger.setLevel(level)
        cls.logger.addHandler(cls.handler)

        return cls
