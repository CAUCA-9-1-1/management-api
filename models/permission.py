from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.database import Database
from ..models.webuser import Webuser

Base = declarative_base()


class PermissionSystem(Base):
	__tablename__ = "tbl_permission_system"

	id_permission_system = Column(String(36), primary_key=True)
	description = Column(String(400))


class PermissionSystemFeature(Base):
	__tablename__ = "tbl_permission_system_feature"

	id_permission_system_feature = Column(String(36), primary_key=True)
	id_permission_system = Column(String(36), ForeignKey(PermissionSystem.id_permission_system), nullable=False)
	feature_name = Column(String(50))
	description = Column(String(255))
	default_value = Column(Boolean, default=False)


class PermissionObject(Base):
	__tablename__ = "tbl_permission_object"

	id_permission_object = Column(String(36), primary_key=True)
	id_permission_object_parent = Column(String(36))
	id_permission_system = Column(String(36), ForeignKey(PermissionSystem.id_permission_system), nullable=False)
	object_table = Column(String(255))
	generic_id = Column(String(36))
	is_group = Column(Boolean)
	group_name = Column(String(255))

	@hybrid_property
	def children(self):
		with Database() as db:
			data = db.query(PermissionObject).filter(PermissionObject.id_permission_object_parent == self.id_permission_object).all()

		return data if data else None

	@hybrid_property
	def text(self):
		if self.is_group:
			return self.group_name
		else:
			with Database() as db:
				webuser = db.query(Webuser).filter(Webuser.id_webuser == self.generic_id).first()

				if webuser:
					return webuser.username

		return ''

class Permission(Base):
	__tablename__ = "tbl_permission"

	id_permission = Column(String(36), primary_key=True)
	id_permission_object = Column(String(36), ForeignKey(PermissionObject.id_permission_object), nullable=False)
	id_permission_system = Column(String(36), ForeignKey(PermissionSystem.id_permission_system), nullable=False)
	id_permission_system_feature = Column(
		String(36),
	    ForeignKey(PermissionSystemFeature.id_permission_system_feature),
	    nullable=False
	)
	access = Column(Boolean, default=None)
	created_on = Column(DateTime, default=datetime.now)

	def __init__(self, id_permission, id_permission_object, id_permission_system, id_permission_system_feature, access):
		self.id_permission = id_permission
		self.id_permission_object = id_permission_object
		self.id_permission_system = id_permission_system
		self.id_permission_system_feature = id_permission_system_feature
		self.access = access