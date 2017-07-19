# coding: utf-8

import pymysql.cursors
from lib.cfg import Cfg
from lib.log import Log


class DB(object):

    conn = None
    _db = None
    _cfg = None

    def __init__(self):
        pass

    @classmethod
    def connect(cls, db='db_pornhub'):

        if DB._db and db != DB._db:
            cls.close()

        DB._db = db
        if not DB._db:
            raise AttributeError('db cannot be None')

        if not DB.conn:
            cfg_parser = Cfg.load()
            if not cfg_parser.has_section(db):
                raise AttributeError('db conf not found')
            DB._cfg = dict(cfg_parser.items(db))

            # Connect to the database
            connection = pymysql.connect(host=DB._cfg['db_host'],
                                         user=DB._cfg['db_user'],
                                         password=DB._cfg['db_password'],
                                         database=DB._cfg['db_name'],
                                         port=int(DB._cfg['db_port']),
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            DB.conn = connection

        return cls

    @classmethod
    def execute(cls, sql, replace_vars=None):
        if not DB.conn:
            raise AttributeError('mysql connection lost')

        result = None
        with DB.conn.cursor() as cursor:
            try:
                result = cursor.execute(sql, replace_vars)
            except:
                Log.err('[sql execute error](' + cursor.mogrify(sql, replace_vars) + ')')
        DB.conn.commit()

        return result

    @classmethod
    def fetch_all(cls, sql, replace_vars=None):
        if not DB.conn:
            raise AttributeError('mysql connection lost')

        with DB.conn.cursor() as cursor:
            cursor.execute(sql, replace_vars)
            result = cursor.fetchall()
        DB.conn.commit()

        return result

    @classmethod
    def fetch_one(cls, sql, replace_vars=None):
        if not DB.conn:
            raise AttributeError('mysql connection lost')
        with DB.conn.cursor() as cursor:
            cursor.execute(sql, replace_vars)
            result = cursor.fetchone()

        DB.conn.commit()

        return result

    @classmethod
    def close(cls):
        if DB.conn:
            try:
                DB.conn.close()
                DB.conn = None
                DB._cfg = None
                DB._db = None
            except:
                pass

    def __del__(self):
        self.close()
