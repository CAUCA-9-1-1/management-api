from api.management.config import setup as config
from cause.api.management.core.manage import Database
from .base import Base
from ..models.permission import PermissionSystemFeature as Table


class PermissionSystemFeature(Base):
	table_name = 'tbl_permission_system_feature'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
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
