import re
from threading import Thread

import pymssql
from DBUtils.PooledDB import PooledDB

from database.settings import X1_CORE_PROD, X1_CORE_DATA


# import sentry_sdk
#
# # sentry报错收集服务器
# sentry_sdk.init("https://89f2e30912c64c1c8b4da5b739e706a8@sentry.io/1876964")

# 装饰器用于使用with开关调用__enter__ 和 __exit__
def db_conn(func):
    def wrapper(self, *args, **kw):
        with self as db:
            result = func(self, db, *args, **kw)
        return result

    return wrapper


# Parameters格式化sql
def format_sql(sql, p):
    parames = []
    if '@' in sql:
        parames = re.findall(r'@\w+', sql)

    for parame in parames:
        sql = sql.replace(parame, "'" + str(p[parame[1:]]) + "'")
    # print(sql)
    return sql


# mssql 结果转换dict
def get_dict(row_list, col_list):
    cols = [d[0] for d in col_list]
    res_list = []
    for row in row_list:
        res_list.append(dict(zip(cols, row)))  # 将两个列表合并成一个字典 dict(zip())方法
    return res_list


class DatabasePool(object):
    def __init__(self, db):
        self.type = db
        if self.type == "X1_CORE_PROD":
            config = {
                'creator': pymssql,
                'host': X1_CORE_PROD['HOST'],
                # 'port': MSSQL['PORT'],
                'user': X1_CORE_PROD['USER'],
                'password': X1_CORE_PROD['PASSWD'],
                'database': X1_CORE_PROD['DB'],
                'charset': X1_CORE_PROD['CHARSET'],
                'maxconnections': 20,  # 连接池最大连接数量
                # 'cursorclass': pymysql.cursors.DictCursor
            }
        else:
            config = {
                'creator': pymssql,
                'host': X1_CORE_DATA['HOST'],
                # 'port': MSSQL['PORT'],
                'user': X1_CORE_DATA['USER'],
                'password': X1_CORE_DATA['PASSWD'],
                'database': X1_CORE_DATA['DB'],
                'charset': X1_CORE_DATA['CHARSET'],
                'maxconnections': 20,  # 连接池最大连接数量
                # 'cursorclass': pymysql.cursors.DictCursor
            }
        self.pool = PooledDB(**config)

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()

    # 查询sql
    @db_conn
    def ExecuteQuery(self, db, sql, p, *args, **kwargs):
        try:
            sql = format_sql(sql, p)
            db.cursor.execute(sql)
            relist = db.cursor.fetchall()
            db.conn.commit()
            if self.type == 'mysql':
                return relist
            else:
                desc_res = db.cursor.description
                return get_dict(relist, desc_res)
        except Exception as e:
            db.conn.rollback()
            return e

    # 非查询的sql
    @db_conn
    def ExecuteNonQuery(self, db, sql, p, *args, **kwargs):
        try:
            sql = format_sql(sql, p)
            db.cursor.execute(sql)
            db.conn.commit()
            print("执行成功！")
        except Exception as e:
            db.conn.rollback()
            return e

    @db_conn
    def ExecuteQueryAsync(self, db, sql, p, *args, **kwargs):
        thread = SqlThread(self.ExecuteQuery, args=(sql, p))
        thread.start()
        thread.join()
        return thread.getResult()

    @db_conn
    def ExecuteNonQueryAsync(self, db, sql, p, *args, **kwargs):
        thread = SqlThread(self.ExecuteNonQuery, args=(sql, p))
        thread.start()
        thread.join()
        # return thread.getResult()


class Parameters(dict):
    def add(self, key, value):
        self.__setitem__(key, value)
        return self


class SqlThread(Thread):
    def __init__(self, func, args=()):
        super(SqlThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.res = self.func(*self.args)

    def getResult(self):
        try:
            return self.res
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # connect = DatabasePool('mysql')
    #
    # lists = connect.ExecQuery('select * from goods_goods limit 3')
    #
    # for i in lists:
    #     print(i)
    #
    # connect.ExecNoQuery("update goods_goods set goods_sn='6666'  where id=52")

    #########
    ##mssql##
    #########
    sql = '''
    select * from mm_item where code = @code
    '''

    p = Parameters().add('code', '1.01.001.020')

    connect = DatabasePool('X1_CORE_PROD')
    lists = connect.ExecuteQueryAsync(sql, p)
    for list in lists:
        print(list)
