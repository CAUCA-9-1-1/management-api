import os
import json
import uuid


def override_each_json_config(existing_config, filename):
	with open(filename) as file:
		configs = json.load(file)

		for key in configs:
			existing_config[key] = configs[key]

def validate_minimal_config():
	if PACKAGE_NAME is None:
		raise Exception("You need to set 'PACKAGE_NAME' inside your config file")

	if PERMISSION is None:
		system_id = str(uuid.uuid4())

		raise Exception("""
			You need to set the permission systemID.
			Place PERMISSION = {'systemID': '%s'} in your config file
			And execute the request "INSERT INTO tbl_permission_system VALUES('%s', '%s');" on your database
		""" % (system_id, system_id, PACKAGE_NAME))


# Database config
DATABASE = None
"""
DATABASE = {
	'general': {
		'engine': '',
		'host': '',
		'dbname': '',
		'username': '',
		'password': '',
	},
	'mysql_winc': {
		'engine': '',
		'host': '',
		'dbname': '',
		'username': '',
		'password': '',
	}
}
"""

# Logs
LOGS_NAME = 'cause-api-management'
LOGS = {
	'level': 'error',
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
MODULE_NAME = 'cause-api-management'
PACKAGE_NAME = None
PACKAGE_VERSION = '__package_version__'
PORT = 8080
SESSION_TIMEOUT = 30

# Page web
CAUSEJS = "st.cauca.ca"
CONTENT_SECURITY_POLICY_CONNECT = None
VERSION = {
	'devExtreme': '16.2.6',
	'jQuery': '3.1.0'
}

# Folder
ROOT = os.path.abspath(os.getcwd())
WEBROOT = '/'
SEARCH_FOLDERS = ['app', 'cause.api.management']

if os.path.isfile("config.json"):
	override_each_json_config(locals(), "config.json")
elif os.path.isfile("config.py"):
	with open("config.py") as file:
		exec(file.read())

validate_minimal_config()
