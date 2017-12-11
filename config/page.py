import os
from . import setup as config
from .base import ConfigBase


class ConfigPage(ConfigBase):
	def __init__(self, specific_base_config=None):
		ConfigBase.__init__(self, specific_base_config)

		if os.path.exists("%s/static" % config.ROOT):
			self.add_config({
				'/static': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': 'static'
				}
			})

	def complete(self):
		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'root')):
			self.add_page('Root', '/')

		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'js')):
			self.add_page('Js')

		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'ajax')):
			self.add_page('Ajax')

		if config.IS_UWSGI is False and config.CACHE_MANIFEST:
			self.add_page('Manifest')

		ConfigBase.complete()