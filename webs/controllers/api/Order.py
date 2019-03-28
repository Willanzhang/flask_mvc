# coding=utf-8
from webs.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.member.oauth_member_bind import OauthMemberBind
from common.libs.UrlManager import UrlManager
from common.libs.pay.PayService import PayService
from common.libs.cart.CartService import CartService
from application import app, db
from common.libs.pay.WeChatService import WeChatService
import json,decimal

@route_api.route("/order/info", methods=["POST"])
def orderInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None
    memeber_info = g.member_info
    params_goods_list = []
    if params_goods:
        params_goods_list = json.loads(params_goods)

    food_dic = {}
    for item in params_goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    # 运费
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tem_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "pic_url": UrlManager.buildImageUrl(item.main_image),
                "number": food_dic[item.id]
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(tem_data)
    default_address = {
        "name": "这是一个大帅哥",
        "mobile": "1567788221",
        "address": "深圳市南山区XX",
    }

    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['default_address'] = default_address
    return jsonify(resp)

@route_api.route("/order/create", methods=["POST"])
def orderCreate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    type = req['type'] if 'type' in req else ''
    params_goods = req['goods'] if 'goods' in req else None

    if params_goods:
        items = json.loads(params_goods)

    if len(items) <1:
        resp['code'] = -1
        resp['msg'] = "下单失败：没有选择商品"
        return jsonify(resp)

    # 下单先在主表添加一个数据，再在副表添加数据

    member_info = g.member_info
    params = {}
    target = PayService()
    resp = target.createOrder(member_info.id, items, params)

    if resp['code'] == 200 and type == "cart":
        CartService.deleteItem(member_info.id, items)

    return jsonify(resp)

@route_api.route("/order/pay", methods=["POST"])
def orderPay():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试"
        return jsonify(resp)

    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试"
        return jsonify(resp)

    config_mina = app.config["MINA_APP"]

    # 支付完后 wechat 会调取我们的回调接口， 解析后我们能获取支付状态
    notify_url = app.config['APP']['domain'] + config_mina['callback_url']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    data = {
        "appid": config_mina['appid'],
        "mch_id": config_mina['mch_id'],
        "nonce_str": target_wechat.get_nonce_str(),
        "body": "订餐",
        "out_trade_no": pay_order_info.order_sn,
        "total_fee": int(pay_order_info.total_price * 100),
        "notify_url": notify_url,
        "trade_type": "JSAPI",
        "openid": oauth_bind_info.openid
    }
    pay_info = target_wechat.get_pay_info(data)

    if pay_info:
        #保存prepay_id 为后面发模板消息
        pay_order_info.prepay_id = pay_info['prepay_id']

        db.session.add(pay_order_info)
        db.session.commit()

        resp['data']['pay_info'] = pay_info

    return jsonify(resp)

# 支付后微信返回结果 在此处理  判断是否是此系统订单，金额是否对
@route_api.route("/order/callback", methods=["POST"])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    header = {'Content-Type': 'application/xml'}
    config_mina = app.config['MINA_APP']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict(request.data)
    # 对比sign 值 防止伪造
    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_wechat.create_sign(callback_data)
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = "FAIL"
        return target_wechat.dict_to_xml(result_data),header

    order_sn = callback_data['out_trade_no']
    # 非法订单
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = "FAIL"
        return target_wechat.dict_to_xml(result_data),header

    # 订单金额对不上
    if int(pay_order_info.total_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = "FAIL"
        return target_wechat.dict_to_xml(result_data), header
    # 订单是处理过的订单
    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    # 进行支付成功我方数据库处理
    target_pay = PayService()
    target_pay.orderSuccess(pay_order_id=pay_order_info.id, params={'pay_sn': callback_data['transaction_id']})

    # 将微信回调的结果放入记录表
    target_pay.addPayCallbackData(pay_order_id=pay_order_info.id, data=request.data)

    return target_wechat