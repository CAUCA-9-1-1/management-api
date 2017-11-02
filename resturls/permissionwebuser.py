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

		id_permission_object_parent = PermissionObject().get_id_permission_object_parent(id_permission_object)

		webuser_permission = Permission().get(id_permission_object)
		parent_permission = Permission().get(id_permission_object_parent)
		
		return webuser_permission if parent_permission else {**webuser_permission, **parent_permission}
