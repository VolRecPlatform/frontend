# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/26 14:35
@Auth ： QX
"""
import random
import string

from flask import Blueprint, render_template, jsonify, redirect, url_for,session
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel, UserModel
from blueprints.forms import RegisterForm, LoginForm
from decorators import login_required

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在！")
                return redirect(url_for("auth.login"))
            if user.password == password:
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user= UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/loginout")
def loginout():
    session.clear()
    return redirect("/")





@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits*4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject="高考平台注册", recipients=[email], body=f"您的验证码为:{captcha}")
    mail.send(message)
    email_captcha =EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"message":"","data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="ceshi",recipients=["1968374004@qq.com"],body="ceshi")
    mail.send(message)
    return "ok"