import uuid
from ..config import setup as config
from ..core.database import Database
from ..models.permission import Permission as Table
from .base import Base
from .permissionsystemfeature import PermissionSystemFeature


class PermissionWebuser(Base):
	table_name = 'tbl_permission'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_permission_object):
		data = ()
		features = PermissionSystemFeature().get()

		if 'data' in features:
			for feature in features['data']:
				feature.webuser_value = None
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
						feature.webuser_value = user_permission.access

				data = data + (feature,)

		return {
			'data': data
		}

	def create(self, args):
		id_permission = uuid.uuid4()

		with Database() as db:
			db.insert(Table(
				id_permission, args['id_permission_object'], args['id_permission_system'],
				args['id_permission_system_feature'], args['webuser_value']
			))
			db.commit()

		return {
			'message': 'permissionwebuser successfully created'
		}

	def modify(self, args):
		if args['id_permission'] is None:
			self.create(args)
		else:
			with Database() as db:
				data = db.query(Table).get(args['id_permission'])

				if 'webuser_value' in args:
					data.access = args['webuser_value']

				db.commit()

		return {
			'message': 'permissionwebuser successfully modified'
		}