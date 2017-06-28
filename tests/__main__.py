import unittest
from ..resturls.base import Base
from .apisaction import TestApisAction
from .auth import TestAuth
from .webuser import TestWebuser
from .webuserstatistic import TestWebuserStatistic


Base.logged_id_webuser = 'd25a7a30-22e0-4169-95b8-bd36368f12d6'


def get_test_api_management(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestApisAction))
	suite.addTest(unittest.makeSuite(TestAuth))
	suite.addTest(unittest.makeSuite(TestWebuser))
	suite.addTest(unittest.makeSuite(TestWebuserStatistic))
	suite.addTest(unittest.makeSuite(TestWebuser))

	return suite