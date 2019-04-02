# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
# 引入统一渲染方法
from common.models.pay.PayOrder import PayOrder
from common.models.food.Food import Food
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import ops_render
from common.libs.Helper import iPagination, selectFilterObj, getDictFilterField, getDictListFilterField
from application import app, db

route_finance = Blueprint( 'finance_page',__name__ )

@route_finance.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    query = PayOrder.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(PayOrder.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={0}".format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    # 查询订单表
    pay_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    data_list = []
    if pay_list:
        # [id, ...ids]
        pay_order_ids = selectFilterObj(pay_list, 'id')

        # {id_value: [item, item]}
        pay_order_items_map = getDictListFilterField(PayOrderItem,
                                                     PayOrderItem.pay_order_id, 'pay_order_id', pay_order_ids)
        #
        food_mapping = {}

        if pay_order_items_map:
            food_ids = []
            for item in pay_order_items_map:

                tmp_food_ids = selectFilterObj(pay_order_items_map[item], 'food_id')
                tmp_food_ids = {}.fromkeys(tmp_food_ids).keys()
                food_ids = food_ids + list(tmp_food_ids)

            # food_ids里面还有重复的， 要去重   food_ids 在这实际上就是根据pay_order 查询的pay_order_item中所有的食品
            # 单数再去重
            food_mapping = getDictFilterField(Food, Food.id, 'id', food_ids)

        for item in pay_list:
            tmp_data = {
                "id": item.id,
                "status_desc": item.status_desc,
                "order_number": item.order_number,
                "price": str(item.total_price),
                "pay_time": item.pay_time,
                "created_time": item.created_time.strftime("%Y%m%d%H%M%S")
            }
            tmp_foods = []
            tmp_order_items = pay_order_items_map[item.id]
            for tmp_order_item in tmp_order_items:
                tmp_food_info = food_mapping[tmp_order_item.food_id]
                tmp_foods.append({
                    'name': tmp_food_info.name,
                    'quantity': tmp_order_item.quantity
                })

            tmp_data['foods'] = tmp_foods
            data_list.append(tmp_data)

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['pay_status_mapping'] = app.config['PAY_STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("finance/index.html", resp_data)


@route_finance.route( "/pay-info" )
def payInfo():
    return ops_render( "finance/pay_info.html" )

@route_finance.route( "/account" )
def account():
    return ops_render( "finance/account.html" )
