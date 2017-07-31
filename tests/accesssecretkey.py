import unittest
from ..core.database import Database
from ..resturls.accesssecretkey import AccessSecretkey


class TestAccessSecretkey(unittest.TestCase):
	def setUp(self):
		self.secretkey = None

	def test_01_create(self):
		result = AccessSecretkey().create()

		self.__class__.secretkey = result['secretkey']
		self.assertEqual(result['message'], "access secretkey successfully created")

	def test_02_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_access_secretkey WHERE secretkey='%s';" % self.__class__.secretkey)