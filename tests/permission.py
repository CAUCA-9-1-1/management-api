import unittest
from ..core.database import Database
from ..resturls.base import Base
from ..resturls.permission import Permission
from ..resturls.permissionobject import PermissionObject
from ..resturls.permissionsystemfeature import PermissionSystemFeature
from ..resturls.permissionwebuser import PermissionWebuser


class TestPermission(unittest.TestCase):
	def setUp(self):
		self.id_permission_object = None
		self.id_permission_system_feature = None

	def test_01_create_object(self):
		result = PermissionObject().create({
			'object_table': 'webuser',
			'generic_id': Base.logged_id_webuser
		})

		self.__class__.id_permission_object = result['id_permission_object']
		self.assertEqual(result['message'], "permission object successfully created")

	def test_02_create_feature(self):
		result = PermissionSystemFeature().create({
			'feature_name': 'test',
			'description': 'test',
			'default_value': False
		})

		self.__class__.id_permission_system_feature = result['id_permission_system_feature']
		self.assertEqual(result['message'], "permission system feature successfully created")

	def test_03_create_permission(self):
		result = Permission().create({
			'id_permission_object': self.__class__.id_permission_object,
			'id_permission_system_feature': self.__class__.id_permission_system_feature,
			'access': True
		})

		self.__class__.id_permission = result['id_permission']
		self.assertEqual(result['message'], "permission successfully created")

	def test_04_get_permission_webuser(self):
		result = PermissionWebuser().get(Base.logged_id_webuser)

		if 'data' not in result or len(result['data']) == 0:
			self.fail("No permission for this permision webuser")

	def test_05_get_permission_object(self):
		result = PermissionObject().get(self.__class__.id_permission_object)

		if 'data' not in result or len(result['data']) == 0:
			self.fail("No permission system feature for this permision object")

		self.assertEqual(result['data'][0].feature_name, "test")

	def test_06_get_permission(self):
		result = Permission().get(self.__class__.id_permission_object)

		if 'data' not in result or len(result['data']) == 0:
			self.fail("No permission for this permision object")

		for permission in result['data']:
			if permission.feature_name == 'test' and permission.access is True:
				return True

		self.fail("We can't get the last created permission")

	def test_07_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_permission WHERE id_permission::UUID='%s';" % self.__class__.id_permission)
			db.execute("DELETE FROM tbl_permission_system_feature WHERE id_permission_system_feature::UUID='%s';" % self.__class__.id_permission_system_feature)
			db.execute("DELETE FROM tbl_permission_object WHERE id_permission_object::UUID='%s';" % self.__class__.id_permission_object)