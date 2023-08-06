# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/28 14:33
@Auth ： QX
"""
from functools import wraps
from flask import g, redirect, url_for

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner