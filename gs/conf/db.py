# -*- coding:utf-8 -*-
__author__ = 'weijingqi'

# 线上数据库
HOST = '121.41.81.213'
#HOST = '120.27.149.24'
PORT = 3306
USER = 'mi_user'
PASSWD = 'mi_user_123!'
DB = 'mi_test'
CHARSET = 'utf8'
# sqlalchemy 配置 看下面的链接
# http://www.pythondoc.com/flask-sqlalchemy/config.html
# 操作函数 sqlalchemy.sql.operators.ColumnOperators
SQLALCHEMY_ECHO = False
# 设置为true则可以直接查看salalchemy转译成的sql语句
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 多少秒后自动回收连接 3600
SQLALCHEMY_POOL_RECYCLE = 3600

# pool size
SQLALCHEMY_POOL_SIZE = 20
