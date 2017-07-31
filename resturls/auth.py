from .base import Base
from .webuser import Webuser
from ..core.database import Database
from ..core.token import Token
from ..models.access_token import AccessToken
from ..models.apis_action import ApisAction


class Auth(Token, Base):
	expires_in_minutes = 120
	mapping_method = {
		'GET': 'token',
		'PUT': 'logon',
		'POST': 'register',
		'DELETE': '',
		'PATCH': '',
	}

	def token(self, token=None):
		if token is None:
			raise Exception("You need to pass a token id")

		with Database() as db:
			data = db.query(AccessToken).filter(AccessToken.access_token == token).first()

			if data is None or self.valid_token(token) is False:
				raise Exception("Invalid token id")

			user = Webuser().get(data.id_webuser)
			apis = db.query(ApisAction).filter(
				ApisAction.id_webuser == data.id_webuser).order_by(
				ApisAction.action_time.desc()).first()

			data.username = user['data'].username
			data.user_ip = apis.action_ip if apis is not None else None

		return {
			'data': data
		}

	def register(self, args):
		return Webuser().create(args)
