# coding=utf-8
from application import app, db
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderCallbackData import PayOrderCallbackDatum
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import getCurrentDate
from common.libs.food.FoodService import FoodService
import decimal, hashlib, time, random

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
        print(note, '1111111111111111111')
        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price

        # 并发处理 悲观锁  乐观锁
        # 这里使用的是悲观锁 行锁
        try:
            tem_food_list = db.session.query(Food).filter(Food.id.in_(food_id))\
                .with_for_update().all()

            tem_food_stock_mapping = {}
            for tem_item in tem_food_list:
                tem_food_stock_mapping[tem_item.id] = tem_item.stock
            # 订单主表 pay_order
            model_pay_order = PayOrder()

            model_pay_order.order_sn = self.geneOrder()
            model_pay_order.member_id = member_id
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.status = -8   # 未支付
            model_pay_order.express_status = -8
            model_pay_order.created_time = model_pay_order.updated_time = getCurrentDate()
            db.session.add(model_pay_order)

            # 订单从表 pay_order_item
            for item in items:
                tem_left_stock = tem_food_stock_mapping[item['id']]
                if decimal.Decimal(item['price']) < 0:
                    continue
                if int(item['number']) > int(tem_left_stock):
                    # 抛出异常
                    raise Exception("您购买的美食太火爆了，剩余%s,您购买%s" % (tem_left_stock, item['number']))

                tmp_ret = Food.query.filter_by(id=item['id']).update({
                    "stock": int(tem_left_stock) - int(item['number']),
                    "updated_time": getCurrentDate()
                })

                if not tmp_ret:
                    raise Exception("下单失败")

                tmp_pay_item = PayOrderItem()
                tmp_pay_item.pay_order_id = model_pay_order.id
                tmp_pay_item.member_id = member_id
                tmp_pay_item.quantity = item['number']
                tmp_pay_item.price = item['price']
                tmp_pay_item.food_id = item['id']
                tmp_pay_item.note = note

                tmp_pay_item.created_time = tmp_pay_item.updated_time = getCurrentDate()
                db.session.add(tmp_pay_item)
                # 库存变更操作
                print('11111111111111')
                FoodService.setStockChangeLog(item['id'], -int(item['number']), "在线购买")
                print('88888888888888888')
            db.session.commit()
            resp['data'] = {
                "id": model_pay_order.id,
                "order_sn": model_pay_order.order_sn,
                "total_price": str(model_pay_order.total_price),
            }

        except Exception as e:
            # 抛出错误要回滚
            db.session.rollback()
            print(e)
            resp['code'] = -1
            resp['msg'] = "下单失败请重新下单"
            resp['msg'] = str(e)
            pass


        print('999999999999999999')
        return resp

    def geneOrder(self):
        m = hashlib.md5()
        sn = ''
        while True:
            text = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 99999999))
            m.update(text.encode("utf-8"))
            sn = m.hexdigest()
            if not PayOrder.query.filter_by(order_sn=sn).first():
                break
        return sn
