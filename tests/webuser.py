import unittest

from api.management.core.database import Database
from ..resturls.webuser import Webuser


class TestWebuser(unittest.TestCase):
	def setUp(self):
		self.id_webuser = None

	def test_01_create(self):
		result = Webuser().create({
			'username': 'webuser for unittest',
			'password': '1234'
		})

		self.__class__.id_webuser = result['id_webuser']
		self.assertEqual(result['message'], "webuser successfully created")

	def test_02_get(self):
		result = Webuser().get(self.__class__.id_webuser)
		self.assertEqual(result['data'].username, 'webuser for unittest')

	def test_03_modify(self):
		result = Webuser().modify({
			'id_webuser': self.__class__.id_webuser,
			'username': 'webuser for unittest+modify'
		})

		self.assertEqual(result['message'], "webuser successfully modified")

	def test_04_get(self):
		result = Webuser().get(self.__class__.id_webuser)
		self.assertEqual(result['data'].username, 'webuser for unittest+modify')

	def test_05_remove(self):
		result = Webuser().remove(self.__class__.id_webuser)
		self.assertEqual(result['message'], "webuser successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_webuser WHERE id_webuser::UUID='%s';" % self.__class__.id_webuser)