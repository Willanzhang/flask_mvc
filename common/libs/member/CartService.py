# coding = utf-8
import hashlib,base64, random, string
import requests, json
from application import app, db
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate

class CartService(object):

    @staticmethod
    def setItems( member_id =0 , food_id = 0, number = 0):
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