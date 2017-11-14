import hashlib
import hmac
from ..config import setup as config


class Encryption:
	@staticmethod
	def password(password):
		if isinstance(password, int):
			password = str(password)

		secretkey = bytes(config.PACKAGE_NAME, encoding='utf-8')
		hash = hmac.new(secretkey, password.encode('UTF-8'), hashlib.sha256)

		return hash.hexdigest()

	@staticmethod
	def compare_password(password_enter, password_bd):
		return hmac.compare_digest(Encryption.password(password_enter), password_bd)