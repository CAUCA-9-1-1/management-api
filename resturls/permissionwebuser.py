from .base import Base
from .permission import Permission
from .permissionobject import PermissionObject


class PermissionWebuser(Base):
	table_name = 'tbl_permission'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_webuser):
		id_permission_object = PermissionObject().get_id_permission_object('webuser', id_webuser)

		if id_permission_object is None:
			permission_object = PermissionObject().create({
				'object_table': 'webuser',
				'generic_id': id_webuser
			})

			id_permission_object = permission_object['id_permission_object']

		return self.loop_for_parent_permission(Permission().get(id_permission_object), id_permission_object)

	def loop_for_parent_permission(self, permission_object, id_permission_object):
		id_permission_object_parent = PermissionObject().get_id_permission_object_parent(id_permission_object)

		if id_permission_object_parent is None:
			return self.set_default_value_as_access(permission_object)

		permission_object_parent = Permission().get(id_permission_object_parent)

		for permission in permission_object["data"]:
			if permission.access is None:
				parent = self.get_permission_of_parent(permission_object_parent, permission.feature_name)
				permission.access = parent.access
				permission.id_permission = parent.id_permission

		return self.loop_for_parent_permission(permission_object, id_permission_object_parent)

	def get_permission_of_parent(self, permission_object, feature_name):
		for permission in permission_object["data"]:
			if permission.feature_name == feature_name:
				return permission

	def set_default_value_as_access(self, permission_object):
		for permission in permission_object["data"]:
			if permission.access is None:
				permission.access = permission.default_value

		return permission_object