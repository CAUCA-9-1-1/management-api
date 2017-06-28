import unittest
from ..resturls.apisaction import ApisAction


class TestApisAction(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = ApisAction().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
