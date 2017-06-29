from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, DateTime, String


Base = declarative_base()


class AccessSecretkey(Base):
	__tablename__ = "tbl_access_secretkey"

	id_access_secretkey = Column(String(36), primary_key=True)
	id_webuser = Column(String(36))
	application_name = Column(String(50))
	randomkey = Column(String(100))
	secretkey = Column(String(100))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_access_secretkey, id_webuser, application_name, randomkey, secretkey):
		self.id_access_secretkey = id_access_secretkey
		self.id_webuser = id_webuser
		self.application_name = application_name
		self.randomkey = randomkey
		self.secretkey = secretkey
		self.is_active = False