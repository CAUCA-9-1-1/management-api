import cherrypy
from .config.api import ConfigApi
from .core.route_url import RouteUrl
from .core.execute_api_class import ExecuteApiClass


class ApiUrl(ExecuteApiClass):
	def __init__(self):
		super(ApiUrl, self).__init__()

		if 'request.dispatch' in ConfigApi.base_config:
			RouteUrl('/', 'Root', 'ALL', 'index')
			RouteUrl('/accesssecretkey/', 'AccessSecretkey')
			RouteUrl('/auth/', 'Auth')
			RouteUrl('/auth/:token', 'Auth', 'GET', 'token')
			RouteUrl('/apisaction/', 'ApisAction')
			RouteUrl('/permission/', 'Permission')
			RouteUrl('/permission/:id_permission_object', 'Permission')
			RouteUrl('/permissionobject/', 'PermissionObject')
			RouteUrl('/permissionobject/:id_permission_object', 'PermissionObject')
			RouteUrl('/permissionsystem/', 'PermissionSystem')
			RouteUrl('/permissionsystemfeature/', 'PermissionSystemFeature')
			RouteUrl('/permissionwebuser/', 'PermissionWebuser')
			RouteUrl('/webuser/', 'Webuser')
			RouteUrl('/webuser/:id_webuser', 'Webuser')
			RouteUrl('/webuserstatistic/:type/:period_start/:period_end', 'WebuserStatistic')

	@cherrypy.expose
	def index(self, *args, **kwargs):
		return self.call_method('Root', self.get_argument(args, kwargs))

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
	def permission(self, *args, **kwargs):
		return self.call_method('Permission', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionobject(self, *args, **kwargs):
		return self.call_method('PermissionObject', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionsystem(self, *args, **kwargs):
		return self.call_method('PermissionSystem', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionsystemfeature(self, *args, **kwargs):
		return self.call_method('PermissionSystemFeature', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionwebuser(self, *args, **kwargs):
		return self.call_method('PermissionWebuser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuser(self, *args, **kwargs):
		return self.call_method('Webuser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuserstatistic(self, *args, **kwargs):
		return self.call_method('WebuserStatistic', self.get_argument(args, kwargs))
