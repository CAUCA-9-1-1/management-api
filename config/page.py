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

		self.use_local_staticwebcontent()

	def use_local_staticwebcontent(self):
		if os.path.exists("%s/cause/staticweb" % config.ROOT):
			self.add_config({
				'/causestatic': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': 'cause/staticweb'
				}
			})
			self.add_config({
				'/plugins': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': 'plugins'
				}
			})

	def complete(self):
		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'root')):
			self.add_page('Root', '/')

		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'js')):
			self.add_page('Js')

		if os.path.exists("%s/app/%s.py" % (config.ROOT, 'ajax')):
			self.add_page('Ajax')

		ConfigBase.complete()