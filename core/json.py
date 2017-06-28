import json
import uuid
import base64
import decimal
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class JsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime("%Y/%m/%d %H:%M:%S")
		elif isinstance(obj, datetime.date):
			return obj.strftime("%Y/%m/%d")
		if isinstance(obj, datetime.time):
			return obj.strftime("%H:%M:%S")
		elif isinstance(obj, uuid.UUID):
			return str(obj)
		elif isinstance(obj, decimal.Decimal):
			return str(obj)
		elif isinstance(obj, Exception):
			return str(obj)
		elif isinstance(obj, object) and isinstance(obj.__class__, DeclarativeMeta):
			return self.sqlalchemy_to_dict(obj)

		return json.JSONEncoder.default(self, obj)

	@staticmethod
	def sqlalchemy_to_dict(obj):
		fields = {}

		for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
			try:
				data = obj.__getattribute__(field)

				if isinstance(data, bytes):
					encode = base64.encodebytes(data)
					data = "data:;base64,%s" % encode.decode('UTF-8')
				else:
					json.dumps(data, cls=JsonEncoder)

				fields[field] = data
			except:
				fields[field] = None

		return fields