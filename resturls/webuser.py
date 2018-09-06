import uuid
import logging
from .base import Base
from ..core.database import Database
from ..core.password import Password
from ..core.session import Session
from ..models.webuser import Webuser as Table
from .permissionobject import PermissionObject


class Webuser(Base):
    table_name = 'tbl_webuser'
    mapping_method = {
        'GET': 'get',
        'PUT': 'modify',
        'POST': 'create',
        'DELETE': 'remove',
        'PATCH': '',
    }

    def get(self, id_webuser=None, is_active=None):
        """ Return all webuser information

        :param id_webuser: UUID
        :param is_active: BOOLEAN
        """
        with Database() as db:
            if id_webuser is None and is_active is None:
                data = db.query(Table).all()
            elif id_webuser is None:
                data = db.query(Table).filter(Table.is_active == is_active).all()
            else:
                data = db.query(Table).get(id_webuser)

        return {
            'data': data
        }

    def get_attribute(self, key):
        user = self.get(Base.logged_id_webuser)

        if 'data' not in user or user['data'] is None:
            return None
        if user['data'].attributes is None:
            return None
        if key not in user['data'].attributes or user['data'].attributes[key] is None:
            return None

        return user['data'].attributes[key]

    def logon(self, username, password):
        with Database() as db:
            data = db.query(Table).filter(
                Table.username == username
            ).first()

        if data is None:
            return False
        if not Password.validate_ascii_character_set(password):
            return False
        if not Password.compare(password, data.password):
            return False

        Base.logged_id_webuser = data.id_webuser
        return True

    def create(self, body):
        id_webuser = uuid.uuid4()
        is_active = self.has_permission('RightAdmin')

        if 'username' not in body or 'password' not in body:
            raise Exception("You need to pass a 'username' and 'password'")
        if not Password.validate_ascii_character_set(body['password']):
            raise Exception("Password is not in the ASCII character set")

        with Database() as db:
            webuser = Table(id_webuser, body['username'], Password.encryption(body['password']), is_active)
            db.insert(webuser)
            db.commit()

            if 'attributes' in body:
                if 'groupPermission' in body['attributes']:
                    PermissionObject().create({
                        'object_table': 'websuer',
                        'generic_id': id_webuser,
                        'id_permission_object_parent': body['attributes']['groupPermission']
                    })

                webuser.set_attributes(id_webuser, body['attributes'])

        return {
            'id_webuser': id_webuser,
            'message': 'webuser successfully created'
        }

    def modify(self, body):
        if 'id_webuser' not in body:
            raise Exception("You need to pass a id_webuser")

        if self.has_permission('RightAdmin') is False and str(body['id_webuser']) != str(Base.logged_id_webuser):
            self.no_access()

        with Database() as db:
            data = db.query(Table).get(body['id_webuser'])

            if 'username' in body:
                data.username = body['username']
            if 'password' in body:
                if not Password.validate_ascii_character_set(body['password']):
                    raise Exception("Password is not in the ASCII character set")

                data.password = Password.encryption(body['password'])
            if 'is_active' in body:
                data.is_active = body['is_active']
            if 'attributes' in body:
                data.set_attributes(body['id_webuser'], body['attributes'])

            db.commit()

        return {
            'message': 'webuser successfully modified'
        }

    def remove(self, id_webuser):
        with Database() as db:
            data = db.query(Table).get(id_webuser)
            data.is_active = False
            db.commit()

        return {
            'message': 'webuser successfully removed'
        }

    def test(self, arg2, arg1):
        return {
            'message': 'webuser successfully test (%s, %s)' % (arg1, arg2)
        }
