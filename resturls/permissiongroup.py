from ..config import setup as config
from ..core.database import Database
from .base import Base
from ..models.permission import PermissionObject as Table


class PermissionGroup(Base):
    table_name = 'tbl_permission_object'
    mapping_method = {
        'GET': 'get',
        'PUT': '',
        'POST': '',
        'DELETE': '',
        'PATCH': '',
    }

    def get(self):
        """ Return all user permission

		:param id_permission_object: UUID
		:param object_table: String
		:param generic_id: String
		"""
        with Database() as db:
            data = db.query(
                Table.id_permission_object,
                Table.text
            ).filter(
                Table.id_permission_system == config.PERMISSION['systemID'],
                Table.id_permission_object_parent == None,
                Table.object_table == "group"
            ).all()

        result = []
        for x, y in data:
            result.append({
                "id_permission_object": x,
                "text": y,
            })

        return {
            'data': result
        }
