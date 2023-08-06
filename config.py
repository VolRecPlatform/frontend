# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/24 16:31
@Auth ： QX
"""
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'gaokao'
USERNAME = 'root'
PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL= True
MAIL_PORT = 465
MAIL_USERNAME = '1968374004@qq.com'
MAIL_PASSWORD = 'alqdfbpmghcqccbd'
MAIL_DEFAULT_SENDER = '1968374004@qq.com'


SECRET_KEY = "qqewfashnkopliuyj"