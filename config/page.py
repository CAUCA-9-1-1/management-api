import os
from . import setup as config
from .base import ConfigBase


class ConfigPage(ConfigBase):
	def __init__(self, specific_base_config=None):
		ConfigBase.__init__(self, specific_base_config)

		self.causejs_config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'StaticWebContent',
			'tools.staticdir.root': os.path.abspath('../../')
		}

		if os.path.exists("%s/static" % config.ROOT):
			self.add_config({
				'/static': self.static_config,
			})

		self.use_local_staticwebcontent()

	def use_local_staticwebcontent(self):
		if config.MINIMIZE_JS is False:
			if not os.path.exists("%s/../../StaticWebContent" % config.ROOT) and not os.path.exists("%s/../../../StaticWebContent" % config.ROOT):
				raise Exception("We can't find StaticWebContent, set 'MINIMIZE_JS = True' in your config.py")
			if not os.path.exists("%s/../../StaticWebContent" % config.ROOT):
				self.causejs_config['tools.staticdir.root'] = os.path.abspath('../../../')

			self.add_config({
				'/causeJs': self.causejs_config
			})

	def complete(self):
		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'root')):
			self.add_page('Root', '/')

		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'js')):
			self.add_page('Js')

		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'ajax')):
			self.add_page('Ajax')

		ConfigBase.complete(self)