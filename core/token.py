import datetime
import hashlib
import random
import uuid
import cherrypy
from .database import Database
from ..config import setup as config
from ..models.access_secretkey import AccessSecretkey
from ..models.access_token import AccessToken
from ..resturls.base import Base
from ..resturls.webuser import Webuser


class Token:
	def logon(self, args):
		if Webuser().logon(args['username'], args['password']):
			id_access_token = uuid.uuid4()
			access_token = self.generate_token()
			refresh_token = self.generate_token()

			with Database() as db:
				db.insert(AccessToken(id_access_token, Base.logged_id_webuser, access_token, refresh_token, self.expires_in_minutes * 60))
				db.commit()

			return {
				'data': {
					'authorization_type': 'Token',
					'expires_in': (self.expires_in_minutes * 60),
					'access_token': access_token,
					'refresh_token': refresh_token,
					'webuser_id': Base.logged_id_webuser,
				}
			}
		else:
			raise Exception("authentification failed")

	def generate_secretkey(self, name):
		randomkey = str(random.getrandbits(256))
		secretkey = "%s-%s" % (name, randomkey)

		return {
			'randomkey': randomkey,
			'secretkey': hashlib.sha224(secretkey.encode('utf-8')).hexdigest()
		}

	def generate_token(self):
		randomkey = str(random.getrandbits(256))
		secretkey = "%s-%s" % (config.PACKAGE_NAME, randomkey)

		return hashlib.sha224(secretkey.encode('utf-8')).hexdigest()

	def valid_access_from_header(self):
		authorization = cherrypy.request.headers.get('Authorization')
		authorization = authorization if authorization is not None else ''
		secretkey = authorization.replace('Key ', '') if 'Key' in authorization else None
		token = authorization.replace('Token ', '') if 'Token' in authorization else None

		if secretkey is not None:
			return self.valid_secretkey(secretkey)
		elif token is not None:
			return self.valid_token(token)

		return False

	def valid_secretkey(self, key):
		with Database() as db:
			data = db.query(AccessSecretkey).filter(AccessSecretkey.secretkey == key).first()

		if data is None:
			return False

		return True if data.is_active is True else False

	def valid_token(self, token):
		with Database() as db:
			data = db.query(AccessToken).filter(AccessToken.access_token == token).first()

		if data is None:
			return False

		expires = data.created_on + datetime.timedelta(0, data.expires_in)

		if expires > datetime.datetime.now():
			self.active_session(token)

			return True

		return False

	def active_session(self, token):
		with Database() as db:
			data = db.query(AccessToken).filter(AccessToken.access_token == token).first()

		if data:
			Base.logged_id_webuser = data.id_webuser