import re
from sqlalchemy.ext.declarative import DeclarativeMeta
from .json import JsonEncoder

class CaseFormat:
	def object_camel_to_snake(self, data):
		if not isinstance(data, tuple) and not isinstance(data, list) and not isinstance(data, dict):
			return data

		if isinstance(data, tuple):
			new_data = ()

			for pos, val in enumerate(data):
				new_data = new_data + (self.object_camel_to_snake(val),)

			return new_data

		if isinstance(data, list):
			new_data = list()
			for pos, val in enumerate(data):
				new_data.append(self.object_camel_to_snake(val))

			return new_data

		if isinstance(data, dict):
			new_data = dict()

			for old_key in data:
				if sum(1 for c in old_key if c.isupper()):
					key = self.camel_to_snake(old_key)
				else:
					key = old_key

				new_data[key] = self.object_camel_to_snake(data[old_key])

			return new_data

	def object_snake_to_camel(self, data):
		if isinstance(data, object) and isinstance(data.__class__, DeclarativeMeta):
			data = JsonEncoder.sqlalchemy_to_dict(data)

		if not isinstance(data, tuple) and not isinstance(data, list) and not isinstance(data, dict):
			return data

		if isinstance(data, tuple):
			new_data = ()

			for pos, val in enumerate(data):
				new_data = new_data + (self.object_snake_to_camel(val),)

			return new_data

		if isinstance(data, list):
			new_data = list()
			for pos, val in enumerate(data):
				new_data.append(self.object_snake_to_camel(val))

			return new_data

		if isinstance(data, dict):
			new_data = dict()

			for old_key in data:
				if '_' in old_key:
					key = self.snake_to_camel(old_key)
				else:
					key = old_key
	
				new_data[key] = self.object_snake_to_camel(data[old_key])

			return new_data

	def camel_to_snake(self, value):
		return re.sub(r'[A-Z]', lambda x: '_' + x.group(0).lower(), value)

	def pascal_to_snake(self, value):
		return self.camel_to_snake(value)[1:]

	def snake_to_camel(self, value):
		return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), value)