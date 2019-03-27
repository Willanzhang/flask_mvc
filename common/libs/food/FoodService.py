# coding=utf-8
from application import db
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from common.models.food.Food import Food
from common.libs.Helper import getCurrentDate
class FoodService():

    @staticmethod
    def setStockChangeLog(food_id=0, quantity=0, note=''):
        print(food_id, quantity)
        print('22222222222222222222')
        # 库存变更表操作
        if food_id < 1:
            return False

        print('333333333333333')

        food_info = Food.query.filter_by(id=food_id).first()

        if not food_id:
            return False
        print('4444444444444')

        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        # 变更的库存
        model_stock_change.unit = quantity
        model_stock_change.total_stock = food_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()
        print('55555555555555')

        db.session.add(model_stock_change)
        db.session.commit()
        print('666666666')
        return True
