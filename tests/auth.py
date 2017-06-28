import unittest
from ..resturls.auth import Auth


class TestAuth(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_token(self):
		result = Auth().token('3a1e600c306f6be83711cd1bb340b5778c222413ae453421ac016740')

		self.assertEqual(str(result['data'].id_webuser), 'd25a7a30-22e0-4169-95b8-bd36368f12d6')
