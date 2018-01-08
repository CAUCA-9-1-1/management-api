import uuid
from .base import Base
from ..core.database import Database
from ..models.permission import PermissionSystem as Table


class PermissionSystem(Base):
    table_name = 'tbl_permission_system'
    mapping_method = {
        'GET': '',
        'PUT': '',
        'POST': 'create',
        'DELETE': '',
        'PATCH': '',
    }

    def create(self, body):
        if 'description' not in body:
            raise Exception("You need to pass a 'description'")

        id_permission_system = uuid.uuid4()

        with Database() as db:
            db.insert(Table(id_permission_system, body['description']))
            db.commit()

        return {
            'id_permission_system': id_permission_system,
            'message': 'permission system successfully created'
        }
