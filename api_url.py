import json
import cherrypy
from .config import setup as config
from .core.execute_api_class import ExecuteApiClass


class ApiUrl(ExecuteApiClass):
	@cherrypy.expose
	def index(self):
		return json.dumps({
			'name': config.PACKAGE_NAME,
			'version': config.PACKAGE_VERSION
		})

	@cherrypy.expose
	def accesssecretkey(self, *args, **kwargs):
		return self.call_method('AccessSecretkey', self.get_argument(args, kwargs))

	@cherrypy.expose
	def auth(self, *args, **kwargs):
		return self.call_method('Auth', self.get_argument(args, kwargs))

	@cherrypy.expose
	def apisaction(self, *args, **kwargs):
		return self.call_method('ApisAction', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionsystemfeature(self, *args, **kwargs):
		return self.call_method('PermissionSystemFeature', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionobject(self, *args, **kwargs):
		return self.call_method('PermissionObject', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionwebuser(self, *args, **kwargs):
		return self.call_method('PermissionWebuser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuser(self, *args, **kwargs):
		return self.call_method('Webuser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuserstatistic(self, *args, **kwargs):
		return self.call_method('WebuserStatistic', self.get_argument(args, kwargs))
