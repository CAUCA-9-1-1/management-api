from . import setup as config
from .base import ConfigBase


class ConfigApi(ConfigBase):
	def __init__(self, specific_base_config={}):
		specific_base_config.update({
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [
				('Access-Control-Allow-Origin', '*'),
				('Access-Control-Allow-Headers', 'Authorization'),
				('Content-Type', 'text/json, text/html'),
				('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, PATCH'),
			],
		})

		ConfigBase.__init__(self, specific_base_config)

	def complete(self):
		self.add_page('ApiUrl', config.WEBROOT)

		ConfigBase.complete(self)
