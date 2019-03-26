# coding=utf-8
from application import app, db
from common.models.food.Food import Food

import decimal

class PayService():
    def __init__(self):
        pass

    def createOrder(self, member_id, items=None, params=None):
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        # 这里面有下单并发的控制以及 库存的减少
        pay_price = decimal.Decimal(0.00)

        # 无效商品跳过的次数
        continue_cnt = 0
        food_id = []
        for item in items:
            if decimal.Decimal(item['price']) < 0:
                continue_cnt += 1
                continue
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            food_id.append(item['id'])

        if continue_cnt >= len(items):
            resp['code'] = -1
            resp['msg'] = "商品items为空"
            return resp

        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''

        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price

        # 并发处理 悲观锁  乐观锁？
        # 这里使用的是悲观锁
        try:
            pass
        except Exception as e:
            pass


        return resp

