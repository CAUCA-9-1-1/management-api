import cherrypy
from . import setup as config
from .base import ConfigBase


class ConfigApi(ConfigBase):
	def __init__(self, specific_base_config={}, build_routing_object=None):
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

		if build_routing_object is not None:
			dispatcher = cherrypy.dispatch.RoutesDispatcher()

			ConfigBase.base_config.update({
				'request.dispatch': dispatcher
			})

			build_routing_object()

	@staticmethod
	def complete():
		if 'request.dispatch' not in ConfigApi.base_config:
			ConfigApi.add_page('ApiUrl', config.WEBROOT)
		else:
			cherrypy.tree.mount(
				root=None,
				config=ConfigApi.site_config
			)

		ConfigBase.complete()
