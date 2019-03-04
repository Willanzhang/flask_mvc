# coding = utf-8
from application import app
from flask import request, redirect
from common.models.user import User
from common.libs.user import UserService
from common.libs.UrlManager import UrlManager

@app.before_request
def before_request():
    path = request.path
    user_info_login = check_login()

    # 登录页面是不需要验证登录的明天弄
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
    if len(auth_info) !=2:
        return False
    try:
        user_info = User.query .filter_by(uid=auth_info[0]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return True
