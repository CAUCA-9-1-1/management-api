import re
from sqlalchemy.ext.declarative import DeclarativeMeta
from .json import JsonEncoder

class CaseFormat:
	def object_camel_to_snake(self, data):
		new_data = dict()

		for old_key in data:
			if sum(1 for c in old_key if c.isupper()):
				key = self.camel_to_snake(old_key)
			else:
				key = old_key
	
			if isinstance(data[key], list):
				info = list()
				for pos, val in enumerate(data[old_key]):
					info.append(self.object_camel_to_snake(val))
				new_data[key] = info
			elif isinstance(data[key], dict):
				new_data[key] = self.object_camel_to_snake(data[old_key])
			else:
				new_data[key] = data[old_key]
	
		return data

	def object_snake_to_camel(self, data):
		new_data = dict()
	
		if isinstance(data, object) and isinstance(data.__class__, DeclarativeMeta):
			data = JsonEncoder.sqlalchemy_to_dict(data)
	
		if isinstance(data, dict):
			for old_key in data:
				if '_' in old_key:
					key = self.snake_to_camel(old_key)
				else:
					key = old_key
	
				if isinstance(data[old_key], tuple):
					info = ()
					for pos, val in enumerate(data[old_key]):
						info = info + (self.object_snake_to_camel(val),)
					new_data[key] = info
				elif isinstance(data[old_key], list):
					info = list()
					for pos, val in enumerate(data[old_key]):
						info.append(self.object_snake_to_camel(val))
					new_data[key] = info
				elif isinstance(data[old_key], dict):
					new_data[key] = self.object_snake_to_camel(data[old_key])
				else:
					new_data[key] = data[old_key]

		return new_data

	def camel_to_snake(self, value):
		return re.sub(r'[A-Z]', lambda x: '_' + x.group(0).lower(), value)

	def pascal_to_snake(self, value):
		return self.camel_to_snake(value)[1:]

	def snake_to_camel(self, value):
		return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), value)