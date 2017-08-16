from ..config import setup as config
from .base import Base


class Root(Base):
	mapping_method = {
		'GET': 'index',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def index(self):
		return {
			'name': config.PACKAGE_NAME,
			'version': config.PACKAGE_VERSION
		}