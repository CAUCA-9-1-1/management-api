import inspect
from ..config import setup as Config
from ..config.api import ConfigApi
from .execute_api_class import ExecuteApiClass
from .exceptions import *


class RouteUrl(ExecuteApiClass):
    def __init__(self, route, controller, method=None, action=None):
        self.controller = self.load_class(controller)
        self.method = method
        self.action = action

        if Config.WEBROOT != "/":
            route = Config.WEBROOT[0:-1] + route

        if route[-1] == '/':
            ConfigApi.add_route(route.replace('/', '-'), route[0:-1], self, 'execute_custom_url', method)
        ConfigApi.add_route(route.replace('/', '-'), route, self, 'execute_custom_url', method)

    def execute_custom_url(self, **kwargs):
        if cherrypy.request.method == 'OPTIONS':
            return json.dumps({})

        try:
            if not self.has_access(self.controller):
                raise AuthentificationException()

            method_name = self.has_method(self.controller, self.method, self.action)
            if method_name:
                kwargs['body'] = self.get_body()
                execute = getattr(self.controller, method_name or self.action, None)
                args = self.get_ask_parameters(kwargs, inspect.signature(execute))

                return_data = execute(self.controller(), **args)

                return self.encode('RouteUrl', return_data)

            raise PermissionException()
        except Exception as e:
            return_json_error(e)
