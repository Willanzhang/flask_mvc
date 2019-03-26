# coding = utf-8
import hashlib,base64, random, string
import requests, json
from application import app, db
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate
from flask import jsonify

class CartService(object):
    @staticmethod
    def deleteItem( member_id=0, items=None):
        if member_id < 1 or not items:
            return False

        for item in items:
            # 删除也要做 db.session.delete(model) 操作
            model_cart = MemberCart.query.filter(MemberCart.food_id == item['id'], MemberCart.member_id == member_id)\
                .first()
            db.session.delete(model_cart)
            db.session.commit()

        return True

    @staticmethod
    def setItems(member_id=0, food_id=0, number=0):
        if member_id < 1 or food_id < 1 or number < 1:
            return False

        cart_info = MemberCart.query.filter_by(food_id=food_id, member_id=member_id).first()
        if cart_info:
            pass
        else:
            cart_info = MemberCart()
            cart_info.member_id = member_id
            cart_info.created_time = getCurrentDate()

        cart_info.food_id = food_id
        cart_info.quantity = number
        cart_info.updated_time = getCurrentDate()
        db.session.add(cart_info)
        db.session.commit()

        return True
