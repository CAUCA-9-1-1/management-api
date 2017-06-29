import os
import logging
import cherrypy
import importlib
from . import setup as config
from ..core.case_format import CaseFormat


class ConfigBase:
	cherrypy_version = 0

	def __init__(self, specific_base_config=None):
		self.cherrypy_version = int(cherrypy.__version__.split('.', 1)[0])
		self.site_config = {}
		self.base_config = {
			'tools.sessions.on': True,
			'tools.sessions.name': config.PACKAGE_NAME,
			'tools.sessions.storage_path': 'data/sessions',
			'tools.sessions.timeout': config.SESSION_TIMEOUT,
			'tools.sessions.secure': config.IS_SSL,
			'tools.sessions.httponly': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
			'log.screen': False,
		}
		self.static_config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static'
		}

		self.create_basic_folder()
		self.check_uwsgi()
		self.config_session()

		if specific_base_config is not None:
			self.base_config.update(specific_base_config)

		self.add_config({
			'/': self.base_config
		})

	def create_basic_folder(self):
		self.add_folder('data')
		self.add_folder('data/logs')
		self.add_folder('data/sessions')

	def check_uwsgi(self):
		if config.IS_UWSGI is False:
			self.base_config.update({
				'log.access_file': '%s/data/logs/cherrypy_access.log' % config.ROOT,
				'log.error_file': '%s/data/logs/cherrypy_error.log' % config.ROOT,
			})

	def config_session(self):
		if self.cherrypy_version > 8:
			self.base_config.update({
				'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession
			})
		else:
			self.base_config.update({
				'tools.sessions.storage_type': 'File'
			})

	def add_config(self, element):
		self.site_config.update(element)

	def add_folder(self, path):
		if not os.path.exists("%s/%s/" % (config.ROOT, path)):
			os.makedirs("%s/%s/" % (config.ROOT, path))

	def add_page(self, page, path=None):
		for folder in config.SEARCH_FOLDERS:
			page_class = self.add_page_from(folder, page)

			if page_class is not None:
				break

		if page_class is None:
			logging.exception("Can't mount the page: %s, config: %s" % (
				page, self.site_config
			))
		else:
			path = path if path is not None else '/%s' % page.lower()
			cherrypy.tree.mount(page_class(), path, self.site_config)

	def add_page_from(self, folder, page):
		try:
			page_name = "%s.%s" % (folder, CaseFormat().pascal_to_snake(page))

			file = '%s/%s.py' % (config.ROOT, page_name.replace('.', '/'))
			if not os.path.isfile(file) and folder[0:5] == 'cause':
				file = '%s/%s.py' % (config.ROOT[0:config.ROOT.rfind('/')], page_name.replace('.', '/'))

			if os.path.isfile(file):
				page_loaded = importlib.import_module(page_name, '%s.pages' % folder)

				return getattr(page_loaded, page)
			else:
				return None
		except Exception as e:
			logging.exception("Loading exception on page '%s': %s", page_name, e)

			return None

	def complete(self):
		self.add_config({
			'server.environment': 'production' if config.IS_DEV is False else 'test_suite',
			'request.show_tracebacks': config.IS_DEV,
		})