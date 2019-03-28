# coding=utf-8
from application import app, db
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderCallbackData import PayOrderCallbackDatum
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import getCurrentDate
from common.libs.food.FoodService import FoodService
from common.libs.queue.QueueService import QueueService
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
                FoodService.setStockChangeLog(item['id'], -int(item['number']), "在线购买")
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

        return resp

    def orderSuccess(self, pay_order_id=0, params=None):
        '''
        订单付款成功后的操作
        status 变为1 支付成功
        express_status 为-7  付款待发货
        改变销售订单
        :param pay_order_id:
        :param params:
        :return:
        '''
        try:
            pay_order_info = PayOrder.query.filter(id=pay_order_id).first()
            if not pay_order_info or pay_order_info.status not in [-8, -7]:
                return False

            pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
            pay_order_info.status = 1
            pay_order_info.express_status = -7
            pay_order_info.pay_time = getCurrentDate()
            pay_order_info.updated_time = getCurrentDate
            db.session.add(pay_order_info)

            # 插入售卖记录 进行统计
            pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_id).all()
            for order_item in pay_order_items:
                tmp_model_sale_log = FoodSaleChangeLog()
                tmp_model_sale_log.id = order_item.food_id
                tmp_model_sale_log.quantity = order_item.quantity
                tmp_model_sale_log.price = order_item.price
                tmp_model_sale_log.member_id = order_item.member_id
                tmp_model_sale_log.created_time = getCurrentDate()
                db.session.add(tmp_model_sale_log)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return False

        QueueService.addQueue("pay", {
            "member_id": pay_order_info.member_id,
            "pay_order_id": pay_order_info.id,
        })

    def addPayCallbackData(self, pay_order_id=0, type='pay', data=None):
        model_callback = PayOrderCallbackDatum()
        model_callback.pay_order_id = pay_order_id
        if type == "pay":
            model_callback.pay_data = data
            model_callback.refund_data = ''
        else:
            model_callback.pay_data = ''
            model_callback.refund_data = data

        model_callback.created_time = model_callback.updated_time = getCurrentDate()
        db.session.add(model_callback)
        db.session.commit()
        return True

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
