import unittest
from ..resturls.webuserstatistic import WebuserStatistic


class TestWebuserStatistic(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = WebuserStatistic().get('connectionByDate')
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)

	def test_02_get(self):
		result = WebuserStatistic().get('requestByTable')
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)

	def test_03_get(self):
		result = WebuserStatistic().get('error')

		self.assertEqual(result['error'], 'Unknown type of data "error"')
