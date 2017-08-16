import inspect
from ..config import setup as config
from .token import Token
from .case_format import CaseFormat
from .load_class import LoadClass
from .exceptions import *


class ExecuteApiClass(LoadClass):
	def __init__(self):
		pass

	def exec_method(self, name, args):
		class_object = self.load_class(name)

		if not self.has_access(class_object):
			raise AuthentificationException()

		method_name = self.has_method(class_object)
		api_method = getattr(class_object, method_name, None)

		if api_method is None:
			raise Exception("We can't find the method '%s' on class '%s'" % (cherrypy.request.method, name))

		execute = getattr(class_object, 'every_execution', None)
		execute(class_object(), name, cherrypy.request.method, *args)
		args = self.get_ask_parameters(args, inspect.signature(api_method))

		return api_method(class_object(), **args)

	def call_method(self, name, args):
		if cherrypy.request.method == 'OPTIONS':
			return json.dumps({
				'success': True,
				'error': '',
			})

		try:

			return self.encode(self.exec_method(name, args))
		except Exception as e:
			return_json_error(e)

	def encode(self, return_data):
		data = {
			'success': True,
			'error': ''
		}

		if isinstance(return_data, dict) and config.FORCE_CAMELCASE is True:
			return_data = CaseFormat().object_snake_to_camel(return_data)
		if isinstance(return_data, dict):
			return_data = CaseFormat().convert(return_data)

		data.update(return_data)

		return json.dumps(data, cls=JsonEncoder)

	def has_method(self, controller, method=None, action=None):
		if method == cherrypy.request.method:
			return action

		if method is None and action is None:
			method_mapping = getattr(controller, 'mapping_method', None)

			if method_mapping is not None:
				if cherrypy.request.method in method_mapping and method_mapping[cherrypy.request.method]:
					return method_mapping[cherrypy.request.method]

		return action

	def has_access(self, controller):
		try:
			class_name = controller.__name__
		except AttributeError as e:
			class_name = ''

		if Token().valid_access_from_header() is True or (
			class_name == 'AccessSecretkey' and cherrypy.request.method == 'POST'
		):
			return True

		return False

	def get_body(self):
		body = cherrypy.request.body.readlines()

		if body and body[0] is not '':
			return json.loads(body[0].decode('utf-8'))

		return {}

	def get_ask_parameters(self, kwargs, args):
		arguments = {}

		if args:
			for key in args.parameters:
				if key is not 'self':
					if key in kwargs:
						arguments[key] = kwargs[key]
					elif key in kwargs['body']:
						arguments[key] = kwargs['body'][key]
					else:
						arguments[key] = None

		return arguments

	def get_argument(self, args, kwargs):
		arguments = kwargs
		arguments['body'] = self.get_body()

		if args is not ():
			arguments['path'] = args

		if config.FORCE_CAMELCASE:
			return CaseFormat().object_camel_to_snake(arguments)

		return arguments

	def parse_json(self, value):
		try:
			return json.loads(value)
		except:
			pass

		return value

	def convert_argument(self, value):
		if value == '' or value == 'null':
			return None
		elif value == 'true':
			return True
		elif value == 'false':
			return False

		return value
