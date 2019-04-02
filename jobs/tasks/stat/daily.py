# coding=utf8
from application import app, db
from common.libs.Helper import getFormatDate, getCurrentDate
from common.models.member.member import Member
from common.models.pay.PayOrder import PayOrder
from common.models.stat.StatDailyFood import StatDailyFood
from common.models.stat.StatDailyMember import StatDailyMember
from common.models.stat.StatDailySite import StatDailySite
from common.models.food.WxShareHistory import WxShareHistory
from sqlalchemy import func
import random
'''
python manager.py runjob -m stat/daily -a member \ food \ site -p 2019-04-06      # 不传默认是当天
'''


class JobTask():
	def __init(self):
		pass

	def run(self, params):
		act = params['act'] if 'act' in params else ''
		date = params['param'][0] if params['param'] and len(params['param']) > 1 else getFormatDate(format="%Y-%m-%d")
		app.logger.info(act)
		if not act:
			return
		date_from = date + " 00-00-00"
		date_to = date + " 23-59-59"

		func_params = {
			'date': date,
			'act': act,
			'date_from': date_from,
			'date_to': date_to
		}

		if act == 'member':
			self.statMember(func_params)
		elif act == 'food':
			pass
		elif act == 'site':
			pass

		'''
		会员统计
		'''
	def statMember(self, params):
		date = params['date']
		date_from = params['date_from']
		date_to = params['date_to']
		act = params['act']
		app.logger.info("act:{0}, from:{1}, to:{2}".format(act, date_from, date_to))

		# 用户数量很大的时候 可以通过命令行多起几个job任务   多进程求mo?
		member_list = Member.query.all()

		if not member_list:
			app.logger.info("no member list")
			return

		for member_info in member_list:
			# StatDailyMember 中每一天每一个人只有一条数据
			tmp_stat_member = StatDailyMember.query.filter_by(date=date, member_id=member_info.id).first()
			if tmp_stat_member:
				tmp_model_stat_member = tmp_stat_member
			else:
				tmp_model_stat_member = StatDailyMember()
				tmp_model_stat_member.member_id = member_info.id
				tmp_model_stat_member.date = date
				tmp_model_stat_member.created_time = getCurrentDate()

			tmp_stat_pay = db.session.query(func.sum(PayOrder.total_price).label("total_pay_money"))\
				.filter(PayOrder.member_id == member_info.id, PayOrder.status == 1)\
				.filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to)\
				.first()

			tmp_stat_share_count = WxShareHistory.query.filter(PayOrder.member_id == member_info.id) \
				.filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to)\
				.count()

			tmp_model_stat_member.total_shared_count = tmp_stat_share_count
			tmp_model_stat_member.total_pay_money = tmp_stat_pay[0] if tmp_stat_pay[0] else 0.00
			'''
			为了测试效果模拟数据
			'''
			# tmp_model_stat_member.total_shared_count = random.randint(50, 100)
			# tmp_model_stat_member.total_pay_money = random.randint(1000, 1010)
			tmp_model_stat_member.updated_time = getCurrentDate()
			db.session.add(tmp_model_stat_member)
			db.session.commit()

		return

