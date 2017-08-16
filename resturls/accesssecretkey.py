import uuid
from ..config import setup as config
from ..core.database import Database
from ..core.token import Token
from ..models.access_secretkey import AccessSecretkey as Table
from .base import Base


class AccessSecretkey(Base):
	mapping_method = {
		'GET': '',
		'PUT': '',
		'POST': 'create',
		'DELETE': '',
		'PATCH': '',
	}

	def create(self):
		""" Create new access secret key
		"""
		id_access_secretkey = uuid.uuid4()
		id_webuser = Base.logged_id_webuser or None
		keys = Token().generate_secretkey(config.PACKAGE_NAME)

		with Database() as db:
			db.insert(Table(id_access_secretkey, id_webuser, config.PACKAGE_NAME,
			                keys['randomkey'], keys['secretkey']))
			db.commit()

		return {
			'secretkey': keys['secretkey'],
			'message': 'access secretkey successfully created'
		}
