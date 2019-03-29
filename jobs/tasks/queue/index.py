# coding=utf-8
from application import app, db
from common.models.food.Food import Food
from common.models.queue.QueueList import QueueList
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.pay.PayOrder import PayOrder
from common.models.member.oauth_member_bind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.pay.WeChatService import WeChatService
import json, requests
'''
python manager.py runjob -m queue/index
'''
class JobTask():
	def __init__(self):
		pass

	def run(self, params):
		list = QueueList.query.filter_by(status=-1) \
			.order_by(QueueList.id.asc()).limit(1).all()
		for item in list:
			if item.queue_name == "pay":
				self.handlePay(item)

			# item.status = 1
			# item.updated_time = getCurrentDate()
			# db.session.add(item)
			# db.session.commit()

	def handlePay(self, item):
		'''
		发送模板消息
		:param item:
		:return:
		'''
		data = json.loads(item.data)
		if 'member_id' not in data or 'pay_oder_id' not in data:
			return False

		pay_order_info = PayOrder.query.filter_by(id=data['pay_oder_id']).first()
		if not pay_order_info:
			return False

		# 查询是否需要是否是绑定用户  需要openid 发送模板
		oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data['member_id']).first()
		if not oauth_bind_info:
			return False

		#  拼接模板需要的信息
		pay_order_item = PayOrderItem.query.filter_id(id=pay_order_info.id).all()
		notice_content = []
		if pay_order_item:
			for item in pay_order_item:
				tmp_food_info = Food.query.filter_by(id=item.food_id).first()
				if not tmp_food_info:
					continue
				notice_content.append("%s %s份" % (tmp_food_info.name, item.quantity))

		keyword1_val = pay_order_info.note if pay_order_info.note else '无'
		keyword2_val = "、".join(notice_content)
		keyword3_val = str(pay_order_info.total_price)
		keyword4_val = str(pay_order_info.order_number)
		keyword5_val = "北京市"

		# 获取access_token
		target_wechat = WeChatService()
		access_token = target_wechat.get_access_token()
		headers = { 'Content-Type': 'application/json'}
		url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token
		params = {
			"touser": oauth_bind_info['openid'],
			"template_id": "WKdxNY93tMi19cLClxp2AK7FIlD_Ma9cQvWC3ODUPdo",
			"page": "pages/my/order_list",
			"form_id": pay_order_info.prepay_id,
			"data": {
				"keyword1": {
					"value": keyword1_val
				},
				"keyword2": {
					"value": keyword2_val
				},
				"keyword3": {
					"value": keyword3_val
				},
				"keyword4": {
					"value": keyword4_val
				},
				"keyword5": {
					"value": keyword5_val
				}
			}
		}

		r = requests.post(url=url, data=json.dumps(params), headers=headers)
		r.encoding = "utf-8"
		app.logger.info(r.text)
		return True

