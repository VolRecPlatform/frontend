# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/26 9:40
@Auth ： QX
"""
from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ ='user'
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class EmailCaptchaModel(db.Model):
    __tablename__ ='email_captcha'
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


class ScoreprovinceModel(db.Model):
    __tablename__ ='score_province'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False)
    province_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100))
    min_section = db.Column(db.String(100), nullable=False)
    min_bigint = db.Column(db.String(100), nullable=False)
    local_batch_name = db.Column(db.Text, nullable=False)
    proscore = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)


class ProvinceModel(db.Model):
    __tablename__ ='province_code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province_id = db.Column(db.Integer, nullable=False)
    province_name = db.Column(db.Text, nullable=False)

class SchoolModel(db.Model):
    __tablename__ ='school_code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False)
    school_name = db.Column(db.Text, nullable=False)


class ScorespecilModfel(db.Model):
    __tablename__ ='score_specil'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100))
    max = db.Column(db.String(100), nullable=True)
    min = db.Column(db.String(100), nullable=False)
    min_section = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    spe_id = db.Column(db.String(100), nullable=False)
    level1_name = db.Column(db.Text, nullable=False)
    spname = db.Column(db.Text, nullable=False)
    local_batch_name = db.Column(db.Text, nullable=False)
    year = db.Column(db.String(100), nullable=False)







