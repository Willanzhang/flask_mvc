# coding = utf-8
from webs.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
from common.models.member.member import Member
from common.models.member.oauth_member_bind import OauthMemberBind
from common.models.food.WxShareHistory import WxShareHistory
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService

@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['mgs'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['mgs'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    gender = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    #  创建表 数据库文件 food.sql
    #  没有openid 才会产生注册这一个动作
    '''
        判断是否已经注册过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        modle_member = Member()
        modle_member.nickname = nickname
        modle_member.gender = gender
        modle_member.avatar = avatar
        modle_member.salt = MemberService.geneSalt()
        modle_member.updated_time = modle_member.created_time = getCurrentDate()
        db.session.add(modle_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = modle_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()
        bind_info = model_bind
        resp['msg'] = "操作成功"
    try:
        member_info = Member.query.filter_by(id=bind_info.member_id).first()
        resp['code'] = 200
        resp['msg'] = "已经绑定"
        resp['data'] = {'nickname': member_info.nickname}
    except Exception:
        resp['code'] = -1
        resp['msg'] = "请重试"
    finally:
        token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
        resp['data'] = {'token': token}
        return jsonify(resp)

@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['mgs'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)
    token ="%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)

@route_api.route("/member/share", methods=[ "POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)





