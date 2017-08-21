import os
import logging
import cherrypy
import importlib
from . import setup as config
from ..core.case_format import CaseFormat


class ConfigBase:
	base_config = {}
	cherrypy_version = 0

	def __init__(self, specific_base_config=None):
		ConfigBase.cherrypy_version = int(cherrypy.__version__.split('.', 1)[0])
		ConfigBase.site_config = {}
		ConfigBase.base_config = {
			'tools.sessions.on': True,
			'tools.sessions.name': config.PACKAGE_NAME,
			'tools.sessions.storage_path': 'data/sessions',
			'tools.sessions.timeout': config.SESSION_TIMEOUT,
			'tools.sessions.secure': config.IS_SSL,
			'tools.sessions.httponly': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
			'log.screen': config.IS_DEV,
		}
		ConfigBase.static_config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static'
		}

		ConfigBase.create_basic_folder()
		ConfigBase.check_uwsgi()
		ConfigBase.config_session()

		if specific_base_config is not None:
			ConfigBase.base_config.update(specific_base_config)

			ConfigBase.add_config({
			'/': ConfigBase.base_config
		})

	@staticmethod
	def create_basic_folder():
		ConfigBase.add_folder('data')
		ConfigBase.add_folder('data/logs')
		ConfigBase.add_folder('data/sessions')

	@staticmethod
	def check_uwsgi():
		if config.IS_UWSGI is False:
			# We skip this configuration on UWSGI because cherrypy open to many log file
			ConfigBase.base_config.update({
				'log.access_file': '%s/data/logs/cherrypy_access.log' % config.ROOT,
				'log.error_file': '%s/data/logs/cherrypy_error.log' % config.ROOT,
			})

	@staticmethod
	def config_session():
		if ConfigBase.cherrypy_version > 8:
			ConfigBase.base_config.update({
				'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession
			})
		else:
			ConfigBase.base_config.update({
				'tools.sessions.storage_type': 'File'
			})

	@staticmethod
	def add_config(element):
		ConfigBase.site_config.update(element)

	@staticmethod
	def add_folder(path):
		if not os.path.exists("%s/%s/" % (config.ROOT, path)):
			os.makedirs("%s/%s/" % (config.ROOT, path))

	@staticmethod
	def add_page(page, path=None):
		for folder in config.SEARCH_FOLDERS:
			page_class = ConfigBase.add_page_from(folder, page)

			if page_class is not None:
				break

		if page_class is None:
			logging.exception("Can't mount the page: %s, config: %s" % (
				page, ConfigBase.site_config
			))
		else:
			path = path if path is not None else '/%s' % page.lower()
			cherrypy.tree.mount(page_class(), path, ConfigBase.site_config)

	@staticmethod
	def add_page_from(package, page):
		try:
			page_name = "%s.%s" % (package, CaseFormat().pascal_to_snake(page))

			file = '%s/%s.py' % (config.ROOT, page_name.replace('.', '/'))
			if not os.path.isfile(file) and package[0:5] == 'cause':
				file = '%s/%s.py' % (config.ROOT[0:config.ROOT.rfind('/')], page_name.replace('.', '/'))

			if os.path.isfile(file):
				page_loaded = importlib.import_module(page_name, package)

				return getattr(page_loaded, page)
			else:
				return None
		except SystemError as e:
			raise Exception("Loading exception on page '%s': %s" % (page_name, e))

	@staticmethod
	def add_route(name, route, controller, action, method=None):
		if 'request.dispatch' in ConfigBase.base_config:
			if method is None or method == 'ALL':
				ConfigBase.base_config['request.dispatch'].connect(
					name=name, route=route, controller=controller, action=action
				)
			else:
				ConfigBase.base_config['request.dispatch'].connect(
					name=name, route=route, controller=controller,
					action=action, conditions={"method": ['OPTIONS', method]}
				)

	@staticmethod
	def complete():
		ConfigBase.add_config({
			'server.environment': 'production' if config.IS_DEV is False else 'test_suite',
			'request.show_tracebacks': config.IS_DEV,
		})