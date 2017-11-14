import hashlib
import hmac
import re
from ..config import setup as config


class Password:
	@staticmethod
	def encryption(password):
		if isinstance(password, int):
			password = str(password)

		secretkey = bytes(config.PACKAGE_NAME, encoding='utf-8')
		hash = hmac.new(secretkey, password.encode('UTF-8'), hashlib.sha256)

		return hash.hexdigest()

	@staticmethod
	def validate(password):
		pattern = re.compile('^[ -~]{8,64}$')

		if not password:
			return False
		if not pattern.match(str(password)):
			return False

		return True

	@staticmethod
	def compare(password_enter, password_bd):
		return hmac.compare_digest(Password.encryption(password_enter), password_bd)