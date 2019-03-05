# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
# 引入统一渲染方法
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.models.user import User
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from application import app, db
from sqlalchemy import or_
route_account = Blueprint('account_page', __name__)

@route_account.route( "/index" )
def index():
    resp_data = {}
    req = request.values

    page = int(req['p']) if ('p' in req and req['p']) else 1

    query = User.query

    # 混合查询要使用到 sqlalchemy 的 or_
    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)
    # 查询status -1 已经删除 1 存在
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))
    # 分页功能
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],  # 想显示多少页 选中页在中间
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    app.logger.info(pages)

    list = query.order_by(User.uid.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resp_data)

@route_account.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id'))
    reback_account = redirect(UrlManager.buildUrl("/account/index"))
    if uid < 1:
        return reback_account

    info = User.query.filter_by(uid=uid).first()
    if not info:
        return reback_account

    resp_data['info'] = info

    return ops_render("account/info.html", resp_data)

@route_account.route( "/set", methods=["GET", "POST"] )
def set():
    default_pwd = "******"
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get('id', 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render("account/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    app.logger.info(req['nickname'])
    nickname = req['nickname'] if 'nickname' in req else None
    mobile = req['mobile'] if 'mobile' in req else None
    email = req['email'] if 'email' in req else None
    login_name = req['login_name'] if 'login_name' in req else None
    login_pwd = req['login_pwd'] if 'login_pwd' in req else None

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名~~'
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的手机号码~~'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的邮箱~~'
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的用户名~~'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的密码~~'
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '该登录名存在，换一个试试呗~~'
        return jsonify(resp)

    # 写入新用户 UserService
    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.login_salt = UserService.geneSalt()
        model_user.created_time = getCurrentDate()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)
