# coding=utf-8
from webs.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from common.libs.UrlManager import UrlManager
from common.libs.pay.PayService import PayService
from common.libs.cart.CartService import CartService
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
    print('------------------')
    print(resp)
    return jsonify(resp)
