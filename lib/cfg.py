# coding: utf-8
import os
import ConfigParser as configparser


class Cfg(object):

    cfgParser = None

    @classmethod
    def load(cls, cfg_path=''):
        if not cls.cfgParser:
            cls.cfgParser = configparser.ConfigParser()

        # 如果文件是一个软链接(symlink), os.path.realpath()可以获取其真实的路径，而os.path.abspath()不可
        # 所执行的起始脚本的路径
        # os.path.curdir() os.getcwd()
        # 脚本文件的绝对路径
        pwd = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.realpath(os.path.join(pwd, os.pardir))
        if not cfg_path:
            cfg_path = os.path.join(root_path, '.env')

        cls.cfgParser.read(cfg_path)
        return cls.cfgParser

    @classmethod
    def get(cls, section, key):
        try:
            cls.cfgParser.get(section, key)
        except configparser.NoOptionError:
            return None
