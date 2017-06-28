import os


# Database config
DATABASE = None
"""
DATABASE = {
	'general': {
		'engine': 'mysql',
		'host': 'bd-dev-maitre',
		'dbname': 'geobase',
		'username': 'usrFireQPhp',
		'password': 'feuQ!123',
	},
	'mysql_winc': {
		'engine': 'mysql',
		'host': 'casrvwincdev',
		'dbname': 'geobase',
		'username': 'admin2',
		'password': 'a9d8m7i6n5qwe',
	}
}
"""

# Logs
LOGS_NAME = 'cause-api'
LOGS = {
	'level': 'info',
	'format': '%(asctime)s:%(name)s/%(funcName)s()@%(lineno)d:%(levelname)s:%(message)s',
}

# Permission in tbl_permission on DB "general"
PERMISSION = None
"""
PERMISSION = {
	'systemID': ''
}
"""

# Host
FORCE_CAMELCASE = False
IS_DEV = False
IS_SSL = False
IS_UWSGI = True
MODULE_NAME = 'opensource'
PACKAGE_NAME = ''
PACKAGE_VERSION = '__package_version__'
PORT = 8080
SESSION_TIMEOUT = 30

# Folder
ROOT = os.path.abspath(os.getcwd())
WEBROOT = '/'
SEARCH_FOLDERS = ['app', 'cause.api.survip', 'cause.api.management']

""" Override all default config with the user config
"""
if os.path.isfile("config.py"):
	with open("config.py") as file:
		exec(file.read())
