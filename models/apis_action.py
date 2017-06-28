import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Text


Base = declarative_base()


class ApisAction(Base):
	__tablename__ = "tbl_apis_action"

	id_apis_action = Column(String(36), primary_key=True)
	id_webuser = Column(String(36))
	method = Column(String(10))
	params = Column(Text)
	action_object = Column(String(50))
	action_object_id = Column(String(36))
	action_time = Column(DateTime, default=datetime.now)

	def __init__(self, id_webuser, method, params, action_object, action_object_id):
		self.id_apis_action = uuid.uuid4()
		self.id_webuser = id_webuser
		self.method = method
		self.params = params
		self.action_object = action_object
		self.action_object_id = action_object_id