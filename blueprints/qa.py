# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/26 14:39
@Auth ： QX
"""
from flask import Blueprint, request, render_template
from models import SchoolModel, ProvinceModel, ScorespecilModfel
import requests
import jsonpath
from decorators import login_required
import math
bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
@login_required
def index():
    schools = SchoolModel.query.order_by((1/SchoolModel.id).desc()).all()
    return render_template("index.html", schools= schools)

@bp.route("/qa/fenshuxian", methods=['GET'])
@login_required
def public_qa():
    i=0
    min_scorelist = []
    min_sectionlist = []
    proscorelist = []
    provincelist = []
    schoollist = []
    jishu = []
    return render_template("fenshuxian.html", schoollist=schoollist, jishu=jishu, proscorelist=proscorelist, min_scorelist=min_scorelist, min_sectionlist=min_sectionlist)

@bp.route("/qa/fenshuxian/jieguo", methods=['GET'])
@login_required
def public_jieguo():
    i=0
    province_name = request.args.get('province')
    special = request.args.get('special')
    chazao = ProvinceModel.query.filter(ProvinceModel.province_name.contains(province_name)).first()
    province_id = chazao.province_id
    if special == '文科':
        type=2
    else :
        type=1
    url = f"http://47.115.212.138/data/predict/{type}/{province_id}"
    r = requests.get(url)
    min_scorelist = {}
    min_sectionlist = {}
    proscorelist = {}
    provincelist = {}
    schoollist = {}
    provincelist2 = {}
    schoollist2 = {}
    jishu = {}
    # 运用jsonpath.jsonpath(字典数据, 路径)
    min_scorelist = jsonpath.jsonpath(r.json(), '$..min_score')
    min_sectionlist = jsonpath.jsonpath(r.json(), '$..min_section')
    proscorelist = jsonpath.jsonpath(r.json(), '$..proscore')
    provincelist = jsonpath.jsonpath(r.json(), '$..province_id')
    schoollist = jsonpath.jsonpath(r.json(), '$..school_id')
    provincelist2 = jsonpath.jsonpath(r.json(), '$..province_id')
    schoollist2 = jsonpath.jsonpath(r.json(), '$..school_id')

    while i < len(schoollist):
        school = SchoolModel.query.filter(SchoolModel.school_id == schoollist[i]).first()
        province = ProvinceModel.query.filter(ProvinceModel.province_id == provincelist[i]).first()
        schoollist[i] = school.school_name
        provincelist[i] = province.province_name
        jishu[i] = i
        i += 1

    return render_template("fenshuxian.html", proscorelist=proscorelist, schoollist=schoollist, jishu=jishu, min_scorelist=min_scorelist, min_sectionlist=min_sectionlist, provincelist= provincelist, schoollist2=schoollist2, provincelist2=provincelist2, type=type)


@bp.route("/qa/school/<school_id>")
def qa_school(school_id):
        schools= SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
        jieguo = ScorespecilModfel.query.filter(ScorespecilModfel.school_id == school_id).all()
        return render_template("detail.html", jieguo=jieguo, school_id=school_id, schools=schools)

@bp.route("/qa/school/public/<school_id>",methods=['GET'])
@login_required
def public_school(school_id):
        province_name = request.args.get('province')
        special = request.args.get('special')
        year = request.args.get("year")
        school_id = request.args.get("school_id")
        schools = SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
        chazao = ProvinceModel.query.filter(ProvinceModel.province_name.contains(province_name)).first()
        province_id = chazao.province_id
        jieguo = ScorespecilModfel.query.filter(ScorespecilModfel.school_id == school_id, ScorespecilModfel.year.contains(year), ScorespecilModfel.province.contains(province_id), ScorespecilModfel.spname.contains(special)).all()
        return render_template("detail.html", jieguo=jieguo, school_id=school_id, schools=schools)

@bp.route("/search")
def search():
    q = request.args.get("q")
    schools = SchoolModel.query.filter(SchoolModel.school_name.contains(q)).all()
    return render_template("index.html", schools=schools)


@bp.route("/qa/tuijian", methods=['GET'])
@login_required
def public_tuijian():

    return render_template("tuijian.html")

@bp.route("/qa/fenshuxian/yuce2", methods=['GET'])
@login_required
def public_fenshuxian_yuce2():
    i = 0
    province_name = request.args.get('province')
    school_id = request.args.get('school_id')
    province =ProvinceModel.query.filter(ProvinceModel.province_name ==province_name).first()
    province_id = province.province_id
    type = request.args.get('special')
    url = f"http://47.115.212.138/data/special/predict/{type}/{province_id}/{school_id}"
    r = requests.get(url)
    local_batch_name = {}
    min_score = {}
    min_section = {}
    count1 = {}
    spname = {}
    local_batch_name = jsonpath.jsonpath(r.json(), '$..local_batch_name')
    min_score = jsonpath.jsonpath(r.json(), '$..min_score')
    min_section = jsonpath.jsonpath(r.json(), '$..min_section')
    spname = jsonpath.jsonpath(r.json(), '$..spname')

    school = SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
    province = ProvinceModel.query.filter(ProvinceModel.province_id == province_id).first()
    while i < len(local_batch_name):
        count1[i] = i
        i += 1

    return render_template("zhuangyeyuce.html", school=school, school_id=school_id, count1=count1, min_score=min_score, type=type,min_section=min_section, local_batch_name=local_batch_name, spname=spname, province=province)


@bp.route("/qa/fenshuxian/yuce/<school_id>/<type>/<province_id>")
@login_required
def public_fenshuxian_yuce(school_id, type, province_id):
    i=0
    url = f"http://47.115.212.138/data/special/predict/{type}/{province_id}/{school_id}"
    r = requests.get(url)
    local_batch_name = {}
    min_score = {}
    min_section = {}
    count1 = {}
    spname = {}
    local_batch_name = jsonpath.jsonpath(r.json(), '$..local_batch_name')
    min_score = jsonpath.jsonpath(r.json(), '$..min_score')
    min_section = jsonpath.jsonpath(r.json(), '$..min_section')
    spname = jsonpath.jsonpath(r.json(), '$..spname')

    school = SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
    province = ProvinceModel.query.filter(ProvinceModel.province_id == province_id).first()
    while i<len(local_batch_name):
        count1[i]=i
        i +=1

    return render_template("zhuangyeyuce.html", school=school, school_id=school_id, count1=count1, min_score=min_score, min_section=min_section, local_batch_name=local_batch_name, spname=spname, province=province, type=type)


@bp.route("/qa/tuijian/jieguo", methods=['GET'])
@login_required
def public_tuijian_jieguo():
    i=0
    m=0
    province_name = request.args.get('province')
    special = request.args.get('special')
    chazao = ProvinceModel.query.filter(ProvinceModel.province_name.contains(province_name)).first()
    province_id = chazao.province_id
    score = request.args.get('score')
    rank = request.args.get('rank')
    proscore = request.args.get('proscore')
    xuanze = request.args.get('xuanze')
    if special == '文科':
        type=2
    else:
        type=1
    url = f"http://47.115.212.138/calculate/recommend/{type}/{province_id}/{score}/{rank}/{proscore}"
    r = requests.get(url)
    proscorelist = {}
    provincelist = {}
    provincelist2 = {}
    schoollist2 = {}
    schoollist = {}
    jishu = {}
    count1 = {}
    type_recommend = {}
    gailv = {}
    proscorelist = jsonpath.jsonpath(r.json(), '$..proscore')
    provincelist = jsonpath.jsonpath(r.json(), '$..province_id')
    schoollist = jsonpath.jsonpath(r.json(), '$..school_id')
    provincelist2 = jsonpath.jsonpath(r.json(), '$..province_id')
    schoollist2 = jsonpath.jsonpath(r.json(), '$..school_id')
    type_recommend = jsonpath.jsonpath(r.json(), '$..type_recommend')
    gailv = jsonpath.jsonpath(r.json(),'$..possibility')
    result1 = type_recommend.count(1)
    result2 = type_recommend.count(2)
    result3 = type_recommend.count(3)
    if xuanze == 'all':
        k=0
        while k < len(schoollist):
            count1[k] = k
            k +=1
    elif xuanze == 'a':
        k=0
        while k<result1:
            count1[k]=k
            k +=1
    elif xuanze == 'b':
        k=result1
        while k<result1+result2:
            count1[m]=k
            k += 1
            m += 1
    elif xuanze == 'c':
        k=result1+result2
        while k<result1+result2+result3:
            count1[m]=k
            k +=1
            m +=1
    while i < len(schoollist):
        school = SchoolModel.query.filter(SchoolModel.school_id == schoollist[i]).first()
        province = ProvinceModel.query.filter(ProvinceModel.province_id == provincelist[i]).first()
        if school is not None:
          schoollist[i] = school.school_name
          provincelist[i] = province.province_name
        gailv[i] = gailv[i]*100

        if gailv[i] ==100:
            gailv[i]=99
        if type_recommend[i] == 1:
             type_recommend[i] = '可保底'
        elif type_recommend[i] == 2:
             type_recommend[i] = '较稳妥'
        elif type_recommend[i] == 3:
             type_recommend[i] = '可冲刺'
        jishu[i] = i
        i += 1

    return render_template("tuijian.html",type=type, proscorelist=proscorelist, schoollist=schoollist, jishu=jishu, type_recommend=type_recommend,  provincelist=provincelist, count1=count1, gailv=gailv, math=math, score=score, proscore=proscore, rank=rank, provincelist2=provincelist2, schoollist2=schoollist2)

@bp.route("/qa/tuijian/jieguo/<type>/<province_id>/<school_id>/<score>/<rank>/<proscore>")
@login_required
def public_tuijian_zhaungye(type, province_id, school_id, score, rank, proscore):
    i=0
    m=0
    xuanze = 'all'
    url = f"http://47.115.212.138/calculate/special/recommend/{type}/{province_id}/{school_id}/{score}/{rank}/{proscore}"
    r = requests.get(url)
    local_batch_namelist = {}
    provincelist = {}
    spname = {}
    jishu = {}
    count1 = {}
    type_recommend = {}
    gailv = {}
    school = SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
    local_batch_namelist = jsonpath.jsonpath(r.json(), '$..local_batch_name')
    provincelist = jsonpath.jsonpath(r.json(), '$..province_id')
    spnamelist = jsonpath.jsonpath(r.json(), '$..spname')
    type_recommend = jsonpath.jsonpath(r.json(), '$..type_recommend')
    gailv = jsonpath.jsonpath(r.json(),'$..possibility')
    result1 = type_recommend.count(1)
    result2 = type_recommend.count(2)
    result3 = type_recommend.count(3)
    if xuanze == 'all':
        k=0
        while k < len(local_batch_namelist):
            count1[k] = k
            k +=1
    elif xuanze == 'a':
        k=0
        while k<result1:
            count1[k]=k
            k +=1
    elif xuanze == 'b':
        k=result1
        while k<result1+result2:
            count1[m]=k
            k += 1
            m += 1
    elif xuanze == 'c':
        k=result1+result2
        while k<result1+result2+result3:
            count1[m]=k
            k +=1
            m +=1
    while i < len(local_batch_namelist):
        province = ProvinceModel.query.filter(ProvinceModel.province_id == provincelist[i]).first()
        if school is not None:
          provincelist[i] = province.province_name
        gailv[i] = gailv[i]*100

        if gailv[i] ==100:
            gailv[i]=99
        if type_recommend[i] == 1:
             type_recommend[i] = '可保底'
        elif type_recommend[i] == 2:
             type_recommend[i] = '较稳妥'
        elif type_recommend[i] == 3:
             type_recommend[i] = '可冲刺'
        jishu[i] = i
        i += 1

    return render_template("zhaungyetuijian.html", spname=spnamelist, school=school, local_batch_namelist=local_batch_namelist, school_id=school_id, jishu=jishu, type_recommend=type_recommend,  provincelist=provincelist, count1=count1, gailv=gailv, math=math, type=type, province_id=province_id, score=score, rank=rank, proscore=proscore)

@bp.route("/qa/tuijian2/jieguo", methods=['GET'])
@login_required
def public_tuijian_zhaungye2():
    type = request.args.get("special")
    province_id = request.args.get("province")
    school_id = request.args.get("school_id")
    score = request.args.get("score")
    rank = request.args.get("rank")
    proscore = request.args.get("proscore")
    xuanze = request.args.get("xuanze")
    i=0
    m=0
    url = f"http://47.115.212.138/calculate/special/recommend/{type}/{province_id}/{school_id}/{score}/{rank}/{proscore}"
    r = requests.get(url)
    local_batch_namelist = {}
    provincelist = {}
    spname = {}
    jishu = {}
    count1 = {}
    type_recommend = {}
    gailv = {}
    school = SchoolModel.query.filter(SchoolModel.school_id == school_id).first()
    local_batch_namelist = jsonpath.jsonpath(r.json(), '$..local_batch_name')
    provincelist = jsonpath.jsonpath(r.json(), '$..province_id')
    spnamelist = jsonpath.jsonpath(r.json(), '$..spname')
    type_recommend = jsonpath.jsonpath(r.json(), '$..type_recommend')
    gailv = jsonpath.jsonpath(r.json(),'$..possibility')
    result1 = type_recommend.count(1)
    result2 = type_recommend.count(2)
    result3 = type_recommend.count(3)
    if xuanze == 'all':
        k=0
        while k < len(local_batch_namelist):
            count1[k] = k
            k +=1
    elif xuanze == 'a':
        k=0
        while k<result1:
            count1[k]=k
            k +=1
    elif xuanze == 'b':
        k=result1
        while k<result1+result2:
            count1[m]=k
            k += 1
            m += 1
    elif xuanze == 'c':
        k=result1+result2
        while k<result1+result2+result3:
            count1[m]=k
            k +=1
            m +=1
    while i < len(local_batch_namelist):
        province = ProvinceModel.query.filter(ProvinceModel.province_id == provincelist[i]).first()
        if school is not None:
          provincelist[i] = province.province_name
        gailv[i] = gailv[i]*100

        if gailv[i] ==100:
            gailv[i]=99
        if type_recommend[i] == 1:
             type_recommend[i] = '可保底'
        elif type_recommend[i] == 2:
             type_recommend[i] = '较稳妥'
        elif type_recommend[i] == 3:
             type_recommend[i] = '可冲刺'
        jishu[i] = i
        i += 1

    return render_template("zhaungyetuijian.html", spname=spnamelist, school=school, local_batch_namelist=local_batch_namelist, school_id=school_id, jishu=jishu, type_recommend=type_recommend,  provincelist=provincelist, count1=count1, gailv=gailv, math=math, type=type, province_id=province_id, score=score, rank=rank, proscore=proscore)
