from .base import Base
from .webuser import Webuser
from ..core.database import Database
from ..core.token import Token
from ..models.access_token import AccessToken
from ..models.apis_action import ApisAction


class Auth(Token, Base):
	expires_in_minutes = 120
	mapping_method = {
		'GET': 'check_active_user',
		'PUT': 'logon',
		'POST': 'register',
		'DELETE': '',
		'PATCH': '',
	}

	def check_active_user(self, token_id=None, session_id=None):
		if token_id is not None:
			return self.check_active_token(token_id)
		elif session_id is not None:
			return self.check_active_session(session_id)
		else:
			raise Exception("You need to pass a token id or session id")

	def check_active_session(self, session_id):
		with Database() as db:
			data = db.query(AccessToken).filter(AccessToken.session_id == session_id).first()

			if data is None or self.valid_token(data.access_token) is False:
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

	def check_active_token(self, token_id):
		with Database() as db:
			data = db.query(AccessToken).filter(AccessToken.access_token == token_id).first()

			if data is None or self.valid_token(token_id) is False:
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

	def register(self, body):
		return Webuser().create(body)
