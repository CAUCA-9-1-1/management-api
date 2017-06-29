import importlib.util
import json
import logging
import os
import cherrypy
from ..config import setup as config
from .json import JsonEncoder
from .token import Token
from .case_format import CaseFormat


class ExecuteApiClass:
	def load_class(self, name):
		class_object = None

		for folder in config.SEARCH_FOLDERS:
			class_object = self.load_class_from(folder, name)

			if class_object is not None:
				break

		if class_object is None:
			raise Exception("We can't find the class: %s" % name)
		else:
			return class_object

	def load_class_from(self, folder, name):
		class_name = "%s.resturls.%s" % (folder, name.lower())

		file = '%s/%s.py' % (config.ROOT, class_name.replace('.', '/'))
		if not os.path.isfile(file) and folder[0:5] == 'cause':
			file = '%s/%s.py' % (config.ROOT[0:config.ROOT.rfind('/')], class_name.replace('.', '/'))

		if os.path.isfile(file):
			try:
				class_load = importlib.import_module(class_name, '%s.resturls' % folder)
				class_object = getattr(class_load, name)

				return class_object
			except Exception as e:
				raise Exception("Loading exception on class '%s': %s" % (name, e))

		return None

	def exec_method(self, name, args):
		class_object = self.load_class(name)
		method_mapping = getattr(class_object, 'mapping_method', None)
		method_name = cherrypy.request.method.lower()

		if method_mapping is not None:
			if cherrypy.request.method in method_mapping and method_mapping[cherrypy.request.method]:
				method_name = method_mapping[cherrypy.request.method]

		api_method = getattr(class_object, method_name, None)

		if api_method is None:
			raise Exception("We can't find the method '%s' on class '%s'" % (cherrypy.request.method, name))

		if Token().valid_access_from_header() is True or (name == 'Auth' and cherrypy.request.method == 'PUT'):
			execute = getattr(class_object, 'every_execution', None)
			execute(class_object(), name, cherrypy.request.method, *args)

			return api_method(class_object(), *args)
		else:
			return {
				'success': False,
				'login': False,
				'error': "Login failed",
			}

	def call_method(self, name, args):
		if cherrypy.request.method == 'OPTIONS':
			return json.dumps({
				'success': True,
				'error': '',
			})

		try:
			data = {
				'success': True,
				'error': ''
			}
			return_data = self.exec_method(name, args)

			if isinstance(return_data, dict) and config.FORCE_CAMELCASE:
				return_data = CaseFormat().object_snake_to_camel(return_data)

			data.update(return_data)

			return json.dumps(data, cls=JsonEncoder)
		except Exception as e:
			logging.exception("Error from api class")

			return json.dumps({
				'success': False,
				'error': e,
				'data': None
			}, cls=JsonEncoder)

	def get_argument(self, args, kwargs):
		arguments = ()

		try:
			body = cherrypy.request.body.readlines()

			if body[0] is not '':
				args = json.loads(body[0].decode('utf-8'))

				if config.FORCE_CAMELCASE:
					arguments = (CaseFormat().object_camel_to_snake(args),)
				else:
					arguments = (args,)
		except Exception as e:
			if args:
				arguments = ()
				for val in args:
					arguments = arguments + (self.convert_argument(val),)
			if kwargs:
				if config.FORCE_CAMELCASE:
					kwargs = CaseFormat().object_camel_to_snake(self.convert_argument(kwargs))

				arguments = (kwargs,)

		return arguments

	def convert_argument(self, val):
		if val == '' or val == 'null':
			return None
		elif val == 'true':
			return True
		elif val == 'false':
			return False

		return val