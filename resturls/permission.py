import uuid
from ..config import setup as config
from ..core.database import Database
from ..models.permission import Permission as Table
from .base import Base
from .permissionsystemfeature import PermissionSystemFeature


class Permission(Base):
    table_name = 'tbl_permission'
    mapping_method = {
        'GET': 'get',
        'PUT': 'modify',
        'POST': 'create',
        'DELETE': 'remove',
        'PATCH': '',
    }

    def get(self, id_permission_object):
        data = ()
        features = PermissionSystemFeature().get()

        if 'data' in features:
            for feature in features['data']:
                feature.access = None
                feature.id_permission = None
                feature.id_permission_object = id_permission_object

                with Database() as db:
                    user_permission = db.query(Table).filter(
                        Table.id_permission_system == config.PERMISSION['systemID'],
                        Table.id_permission_object == id_permission_object,
                        Table.id_permission_system_feature == feature.id_permission_system_feature
                    ).first()

                    if user_permission is not None:
                        feature.id_permission = user_permission.id_permission
                        feature.access = user_permission.access

                data = data + (feature,)

        return {
            'data': data
        }

    def create(self, body):
        if 'id_permission_object' not in body or 'id_permission_system_feature' not in body or 'access' not in body:
            raise Exception("You need to pass a 'id_permission_object', 'id_permission_system_feature' and 'access'")

        id_permission = uuid.uuid4()

        with Database() as db:
            db.insert(Table(
                id_permission, body['id_permission_object'], config.PERMISSION['systemID'],
                body['id_permission_system_feature'], body['access']
            ))
            db.commit()

        return {
            'id_permission': id_permission,
            'message': 'permission successfully created'
        }

    def modify(self, body):
        if 'id_permission' not in body:
            raise Exception("You need to pass a 'id_permission'")

        with Database() as db:
            data = db.query(Table).get(body['id_permission'])

            if 'access' in body:
                data.access = body['access']

            db.commit()

        return {
            'message': 'permission successfully modified'
        }

    def remove(self, id_permission):
        with Database() as db:
            db.query(Table).filter(Table.id_permission == id_permission).delete()
            db.commit()

        return {
            'message': 'webuser successfully removed'
        }
