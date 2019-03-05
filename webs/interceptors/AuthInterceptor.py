# coding = utf-8
from application import app
from flask import request, redirect, g
from common.models.user import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re

@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNOER_CHECK_LOGIN_URL']
    path = request.path

    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    # 判断是否登录
    user_info_login = check_login()
    g.current_user = None
    if user_info_login:
        g.current_user = user_info_login

    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return
    # 登录页面是不需要验证登录的
    if not user_info_login:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


'''
判断用户是否已经登录
'''


def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query .filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return user_info
