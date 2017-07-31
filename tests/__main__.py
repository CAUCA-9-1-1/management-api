import unittest
from .accesssecretkey import TestAccessSecretkey
from .apisaction import TestApisAction
from .auth import TestAuth
from .permission import TestPermission
from .webuser import TestWebuser
from .webuserstatistic import TestWebuserStatistic


def get_test_api_management(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestAccessSecretkey))
	suite.addTest(unittest.makeSuite(TestApisAction))
	suite.addTest(unittest.makeSuite(TestAuth))
	suite.addTest(unittest.makeSuite(TestPermission))
	suite.addTest(unittest.makeSuite(TestWebuser))
	suite.addTest(unittest.makeSuite(TestWebuserStatistic))
	suite.addTest(unittest.makeSuite(TestWebuser))

	return suite