from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.database import Database
from api.management.core.encryption import Encryption
from api.management.core.utilities import Utilities

Base = declarative_base()


class WebuserAttributes(Base):
	__tablename__ = "tbl_webuser_attributes"

	id_webuser = Column(String(36), primary_key=True)
	attribute_name = Column(String(50), primary_key=True)
	attribute_value = Column(String(200))

	def __init__(self, id_webuser, attribute_name, attribute_value):
		self.id_webuser = id_webuser
		self.attribute_name = attribute_name
		self.attribute_value = attribute_value


class Webuser(Base):
	__tablename__ = "tbl_webuser"

	id_webuser = Column(String(36), primary_key=True)
	username = Column(String(100))
	password = Column(String(100))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def attributes(self):
		with Database() as db:
			attrs = db.query(WebuserAttributes).filter(WebuserAttributes.id_webuser == self.id_webuser).all()

		return Utilities.list_to_dict(attrs, 'attribute_name', 'attribute_value')

	def __init__(self, id_webuser, username, password):
		self.id_webuser = id_webuser
		self.username = username
		self.password = Encryption.password(password)

	def set_attributes(self, id_webuser, attributes):
		with Database() as db:
			for name in attributes:
				data = db.query(WebuserAttributes).filter(
					WebuserAttributes.id_webuser == id_webuser,
					WebuserAttributes.attribute_name == name,
				).first()

				if data:
					data.attribute_value = attributes[name]
				else:
					db.insert(WebuserAttributes(id_webuser, name, attributes[name]))

				db.commit()
