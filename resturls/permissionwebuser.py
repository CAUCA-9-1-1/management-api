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

		return Permission().get(id_permission_object)
