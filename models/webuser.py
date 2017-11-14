import json
import logging
from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from ..core.database import Database
from ..core.password import Password
from ..core.utilities import Utilities


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
			attributes = list()

			for attr in attrs:
				try:
					attr.attribute_value = json.loads(attr.attribute_value)
				except:
					pass

				attributes.append(attr)

			return Utilities.list_to_dict(attributes, 'attribute_name', 'attribute_value')

		return {}

	def __init__(self, id_webuser, username, password, is_active):
		self.id_webuser = id_webuser
		self.username = username
		self.password = Password.password(password)
		self.is_active = is_active

	def set_attributes(self, id_webuser, attributes):
		with Database() as db:
			for name in attributes:
				if isinstance(attributes[name], list):
					attributes[name] = json.dumps(attributes[name])

				data = db.query(WebuserAttributes).filter(
					WebuserAttributes.id_webuser == id_webuser,
					WebuserAttributes.attribute_name == name,
				).first()

				if data:
					data.attribute_value = attributes[name]
				else:
					db.insert(WebuserAttributes(id_webuser, name, attributes[name]))

				db.commit()
