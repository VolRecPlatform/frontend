# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/2 9:47
@Auth ： QX
"""
from flask import Blueprint, request, Flask, g, redirect, url_for
import requests
import jsonpath
def public_qa():
    province_name = 12
    special = '文科'

    province_id = 11
    score =600
    rank = 18000
    proscore = 500
    if special == '文科':
        type_spe = 2
    else :
        type_spe = 1
    url = f"http://47.115.212.138/data/special/predict/1/11/140"
    r = requests.get(url)
    return r.json()



app.run(debug=True)