import json
import logging
import cherrypy
from ..config import setup as config
from .request import Request


class Session:
	@staticmethod
	def get(key):
		if key in cherrypy.session:
			return cherrypy.session[key]

		return None

	@staticmethod
	def set(key, value):
		cherrypy.session[key] = value

	def permission(self, feature_name):
		if Session.get('access_token') is None:
			return False

		query = Request("%s/permissionwebuser/%s" % (config.WEBSERVICE['host'], Session.get('id_webuser')), 'GET')
		data = json.loads(query.send(None, None, {
			'Authorization': 'Token %s' % Session.get('access_token')
		}))

		if 'data' in data and data['data'] is not None:
			for permission in data['data']:
				if permission['feature_name'] == feature_name:
					return True

		return False

	def is_logged(self):
		if Session.get('id_webuser') is not None:
			return True

		return self.reset_session()

	def reset_session(self):
		if not hasattr(config, "WEBSERVICE"):
			return False

		query = Request("%s/auth/" % config.WEBSERVICE['host'], 'GET')
		data = json.loads(query.send({
			'token': None,
			'session_id': cherrypy.session._id
		}, None, {
			'Authorization': 'Key %s' % config.WEBSERVICE['key']
		}))

		return self.config_session(data)

	def logout(self):
		cherrypy.session['id_webuser'] = None
		cherrypy.session['access_token'] = None
		cherrypy.session['refresh_token'] = None

	def logon(self, username, password=''):
		""" Generate a session on server

		:param username: Username of user to open the session
		:param password: Password of user to open the session
		:return: True if the session is valid
		"""
		self.logout()

		if not hasattr(config, "WEBSERVICE"):
			return False
		if config.WEBSERVICE is None:
			raise Exception("""You need to set 'WEBSERVICE' inside your config file
				WEBSERVICE = {
					'host': '',
					'key': ''
				}""")

		query = Request("%s/auth/" % config.WEBSERVICE['host'], 'PUT')
		data = json.loads(query.send({
			'username': username,
			'password': password,
			'session_id': cherrypy.session._id
		}, None, {
			'Authorization': 'Key %s' % config.WEBSERVICE['key']
		}))

		return self.config_session(data)

	def config_session(self, data):
		if 'data' not in data:
			return False
		if data['success'] == False:
			return False

		cherrypy.session['access_token'] = data['data']['access_token']
		cherrypy.session['refresh_token'] = data['data']['refresh_token'] if 'refresh_token' in data['data'] else ''
		cherrypy.session['id_webuser'] = data['data']['id_webuser'] if 'id_webuser' in data['data'] else ''

		return True


	def change_password(self, password):
		data = {
			'id_webuser': cherrypy.session['id_webuser'],
			'password': password,
			'reset_password': '0'
		}

		if 'token' in config.WEBSERVICE:
			query = Request("%s/webuser/" % config.WEBSERVICE['host'], 'PUT')
			query.send(data, None, {
				'Authorization': 'Token %s' % config.WEBSERVICE['access_token']
			})
