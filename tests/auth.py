import unittest
from ..resturls.base import Base
from ..resturls.auth import Auth
from ..core.exceptions import AuthentificationException


class TestAuth(unittest.TestCase):
	def setUp(self):
		self.token = None

	def test_01_logon(self):
		try:
			result = Auth().logon({
				'username': 'test',
				'password': 'testtest'
			})

			self.__class__.token = result['data']['access_token']
		except AuthentificationException:
			self.fail("""You need to create a user 'test' with the password 'testtest'.
						And make sure has all permission to 'false'.""")

	def test_02_token(self):
		if self.__class__.token is not None:
			result = Auth().token(self.__class__.token)

			self.assertEqual(str(result['data'].username), 'test')

	def test_03_set_admin_user(self):
		Base.logged_id_webuser = '1824a885-f0de-4caf-b140-690fc4f987ff'