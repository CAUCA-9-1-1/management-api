import uuid
from ..config import setup as config
from ..core.database import Database
from .base import Base
from ..models.permission import Permission, PermissionSystemFeature, PermissionObject as Table


class PermissionObject(Base):
	table_name = 'tbl_permission_object'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'save',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_permission_object=None, object_table=None, generic_id=None):
		""" Return all user permission

		:param id_permission_object: UUID
		:param object_table: String
		:param generic_id: String
		"""
		if id_permission_object is None and object_table is None and generic_id is None:
			with Database() as db:
				data = db.query(Table).filter(
					Table.id_permission_system == config.PERMISSION['systemID'],
					Table.id_permission_object_parent == None
				).all()
		else:
			if id_permission_object is None and generic_id is not None:
				id_permission_object = self.get_id_permission_object(object_table, generic_id)

			with Database() as db:
				data = db.query(PermissionSystemFeature).filter(
					PermissionSystemFeature.id_permission_system == config.PERMISSION['systemID'],
					Permission.id_permission_system_feature == PermissionSystemFeature.id_permission_system_feature,
					Permission.id_permission_object == id_permission_object
				).all()

		return {
			'data': data
		}

	def create(self, body):
		if 'object_table' not in body or 'generic_id' not in body:
			raise Exception("You need to pass a 'object_table' and 'generic_id'")

		id_permission_object = uuid.uuid4()
		is_group = body['is_group'] if 'is_group' in body else False
		group_name = body['group_name'] if 'group_name' in body else ''

		with Database() as db:
			db.insert(Table(
				id_permission_object, None, config.PERMISSION['systemID'],
				body['object_table'], body['generic_id'], is_group, group_name
			))
			db.commit()

		return {
			'id_permission_object': id_permission_object,
			'message': 'permission object successfully created'
		}

	def save(self, body):
		if 'id_permission' not in body or body['id_permission'] is None:
			if 'id_permission_system_feature' not in body:
				body['id_permission_system_feature'] = self.create_permission_system_feature(body['description'], body['default_value'])

			if 'id_permission_object' not in body or body['id_permission_object'] is None:
				body['id_permission_object'] = self.get_id_permission_object(body['object_table'], body['generic_id'])

			self.create_permission(body['id_permission_object'], body['id_permission_system_feature'], body['access'])
		else:
			self.modify_permission(body['id_permission'], body['access'])

		return {
			'message': 'permission successfully save'
		}

	def get_id_permission_object(self, object_table, generic_id):
		with Database() as db:
			object = db.query(Table).filter(
				Table.object_table == object_table,
				Table.generic_id == generic_id
			).first()

			if object is not None:
				return object.id_permission_object

		return None