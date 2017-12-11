import os
import os.path
import cherrypy
from .config import setup as config


class Manifest:
	@cherrypy.expose
	def index(self, **kwargs):
		""" Generate one javascript file. This eliminate some request to server

		:param kwargs: Request page element (GET or POST)
		:return: HTML code
		"""
		cherrypy.response.headers['Content-Type'] = 'text/cache.manifest'
		content = self.read_manifest()

		return content

	def read_manifest(self):
		file = config.CACHE_MANIFEST[1:]

		if os.path.isfile(file):
			with open(file, 'r', encoding='UTF-8') as file:
				return file.read()


if __name__ == '__main__':
	Manifest().index()
