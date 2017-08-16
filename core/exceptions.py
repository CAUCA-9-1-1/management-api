import json
import logging
import cherrypy
from .json import JsonEncoder


class AuthentificationException(Exception):
	pass


class PermissionException(Exception):
	pass


def return_json_error(e):
	logging.exception("Error from api class")

	if isinstance(e, AuthentificationException):
		cherrypy.response.status = "401 Unauthorized"
	elif isinstance(e, PermissionException):
		cherrypy.response.status = "403 Forbidden"
	else:
		cherrypy.response.status = "400 Bad Request"

	return json.dumps({
		'success': False,
		'error': e,
		'data': None
	}, cls=JsonEncoder)