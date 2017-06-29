from ..config import setup as config
from ..core.database import Database
from .base import Base
from ..models.permission import Permission, PermissionSystemFeature, PermissionObject as Table


class PermissionObject(Base):
	table_name = 'tbl_permission_object'
	mapping_method = {
		'GET': 'get',
		'PUT': 'move',
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

	def move(self, args):
		onUsePermission().set_permission_object_parent(args['id_permission_object'], args['id_permission_object_parent'])

		return {
			'message': 'permission object successfully move'
		}

	def save(self, args):
		if 'id_permission' not in args or args['id_permission'] is None:
			if 'id_permission_system_feature' not in args:
				args['id_permission_system_feature'] = self.create_permission_system_feature(args['description'], args['default_value'])

			if 'id_permission_object' not in args or args['id_permission_object'] is None:
				args['id_permission_object'] = self.get_id_permission_object(args['object_table'], args['generic_id'])

			self.create_permission(args['id_permission_object'], args['id_permission_system_feature'], args['access'])
		else:
			self.modify_permission(args['id_permission'], args['access'])

		return {
			'message': 'permission successfully save'
		}
