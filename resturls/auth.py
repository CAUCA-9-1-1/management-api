from .base import Base
from .webuser import Webuser
from ..core.database import Database
from ..core.token import Token
from ..models.access_token import AccessToken


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

		return {
			'data': data
		}

	def register(self, args):
		Webuser().create(args)

		return {
			'message': 'user successfully saved'
		}
