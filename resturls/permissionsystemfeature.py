import uuid
from .base import Base
from ..config import setup as config
from ..core.database import Database
from ..models.permission import PermissionSystemFeature as Table


class PermissionSystemFeature(Base):
	table_name = 'tbl_permission_system_feature'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, feature_name=None):
		with Database() as db:
			if feature_name is None:
				data = db.query(Table).filter(
					Table.id_permission_system == config.PERMISSION['systemID']
				).all()
			else:
				data = db.query(Table).filter(
					Table.id_permission_system == config.PERMISSION['systemID'],
					Table.feature_name == feature_name
				).all()

		return {
			'data': data
		}

	def create(self, args):
		if 'feature_name' not in args or 'description' not in args or 'default_value' not in args:
			raise Exception("You need to pass a 'feature_name', 'description' and 'default_value'")

		id_permission_system_feature = uuid.uuid4()

		with Database() as db:
			db.insert(Table(
				id_permission_system_feature, config.PERMISSION['systemID'],
				args['feature_name'], args['description'], args['default_value']
			))
			db.commit()

		return {
			'id_permission_system_feature': id_permission_system_feature,
			'message': 'permission system feature successfully created'
		}

	def modify(self, args):
		if 'id_permission_system_feature' not in args:
			raise Exception("You need to pass a 'id_permission_system_feature'")

		with Database() as db:
			data = db.query(Table).get(args['id_permission_system_feature'])

			if 'default_value' in args:
				data.default_value = args['default_value']
			if 'description' in args:
				data.description = args['description']

			db.commit()

		return {
			'message': 'permission system feature successfully modified'
		}