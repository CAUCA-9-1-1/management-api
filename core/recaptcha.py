import json
import logging
import cherrypy
from ..config import setup as config
from .request import Request


class Recaptcha:
	def __init__(self):
		if config.RECAPTCHA_SECRET_KEY is None:
			logging.info('Recaptcha', '__init__', 'You need to set RECAPTCHA_SECRET_KEY in your config')

	def validate(self, response):
		params = {
			'secret': config.RECAPTCHA_SECRET_KEY,
			'response': response,
			'remoteip': cherrypy.request.headers["Remote-Addr"]
		}
		request = Request("https://www.google.com/recaptcha/api/siteverify")
		google_response = json.loads(request.send(params))

		return google_response["success"]