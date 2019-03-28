# coding=utf-8
from application import app, db
from common.models.queue.QueueList import QueueList
from common.libs.Helper import getCurrentDate
import json

class QueueService():
	@staticmethod
	def addQueue(queue_name, data=None):
		model_queue = QueueList()
		model_queue.queue_name = queue_name
		if data:
			model_queue.data = json.loads(data)

		model_queue.created_time = model_queue.updated_time = getCurrentDate()
		db.session.add(model_queue)
		db.session.commit()
		return True
