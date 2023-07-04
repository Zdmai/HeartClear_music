import os

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'HeartClearmusic'
USERNAME = 'root'
PASSWORD = 'zzz'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}: {}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# 创建数据库引擎