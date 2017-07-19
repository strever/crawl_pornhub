# coding: utf-8

import redis

from lib.cfg import Cfg
from lib.log import Log
import pydoc


class RedisHandler(object):

    conn = None
    _which_redis = None
    _cfg = None

    def __init__(self):
        pass

    @classmethod
    def connect(cls, which_redis='redis_default'):

        if not which_redis:
            raise AttributeError('redis cannot be None')

        if RedisHandler._which_redis and which_redis != RedisHandler._which_redis:
            cls.close()

        RedisHandler._which_redis = which_redis

        if not RedisHandler.conn:
            cfg_parser = Cfg.load()
            if not cfg_parser.has_section(which_redis):
                raise AttributeError('redis conf not found')
            RedisHandler._cfg = dict(cfg_parser.items(which_redis))

            # Connect to the database
            print type(redis)
            RedisHandler.conn = redis.StrictRedis(host=RedisHandler._cfg['redis_host'], port=RedisHandler._cfg['redis_port'])

        return RedisHandler.conn

    @classmethod
    def close(cls):
        if RedisHandler.conn:
            try:
                #RedisHandler.conn.close()
                RedisHandler.conn = None
                RedisHandler._cfg = None
                RedisHandler._which_redis = None
            except:
                pass

    def __del__(self):
        self.close()
