import json

from api.management.config import setup as config
from api.management.core.database import Database
from ..models.apis_action import ApisAction as Table
from ..models.permission import Permission, PermissionSystemFeature, PermissionObject


class Base:
	logged_id_webuser = None
	table_name = ''
	mapping_method = {
		'GET': '',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def every_execution(self, class_name, method, *args):
		if self.table_name == '':
			return

		field_id = self.table_name.replace('tbl_', 'id_')
		object_id = None

		if len(args) > 0:
			if field_id in args[0]:
				object_id = args[0][field_id]

		with Database() as db:
			db.insert(Table(Base.logged_id_webuser, method, json.dumps(args), class_name, object_id))
			db.commit()

	def options(self):
		return {}

	def has_permission(self, feature_name):
		with Database() as db:
			permission_object = db.query(PermissionObject).filter(
				PermissionObject.id_permission_system == config.PERMISSION['systemID'],
				PermissionObject.object_table == 'webuser',
				PermissionObject.generic_id == str(Base.logged_id_webuser),
			).first()

			if permission_object:
				webuser = db.query(Permission).filter(
					Permission.id_permission_object == permission_object.id_permission_object,
					Permission.id_permission_system_feature == PermissionSystemFeature.id_permission_system_feature,
					PermissionSystemFeature.feature_name == feature_name,
				).first()

				if webuser is None or webuser.access is None:
					parent = db.query(Permission).filter(
						Permission.id_permission_object == permission_object.id_permission_object_parent,
						Permission.id_permission_system_feature == PermissionSystemFeature.id_permission_system_feature,
						PermissionSystemFeature.feature_name == feature_name,
					).first()

					return parent.access
				else:
					return webuser.access

		return False

	def no_access(self):
		return {
			'error': 'check your access'
		}