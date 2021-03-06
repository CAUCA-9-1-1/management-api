from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AccessToken(Base):
	__tablename__ = "tbl_access_token"

	id_access_token = Column(String(36), primary_key=True)
	id_webuser = Column(String(36))
	access_token = Column(String(100))
	refresh_token = Column(String(100))
	created_on = Column(DateTime, default=datetime.now)
	expires_in = Column(Integer, default=1)
	session_id = Column(String(40))
	logout_on = Column(DateTime)

	def __init__(self, id_access_token, id_webuser, access_token, refresh_token, expires_in, session_id=None):
		self.id_access_token = id_access_token
		self.id_webuser = id_webuser
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.expires_in = expires_in
		self.session_id = session_id