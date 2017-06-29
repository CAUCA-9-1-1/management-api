import logging
import os

from ..config import setup as config


class Logging:
	""" Log some information inside local file
	"""
	def __init__(self):
		if not os.path.exists("%s/%s/" % (config.ROOT, 'data')):
			os.makedirs("%s/%s/" % (config.ROOT, 'data'))

		if not os.path.exists("%s/data/%s/" % (config.ROOT, 'logs')):
			os.makedirs("%s/data/%s/" % (config.ROOT, 'logs'))

		self.activate_logging()
		self.enable_debug_console()

	def activate_logging(self):
		"""Enable file logging in application using the configuration.
		"""
		log_dir = os.path.join(config.ROOT, "data/logs")
		log_file = os.path.join(log_dir, "%s.log" % config.LOGS_NAME)
		log_level_no = getattr(logging, config.LOGS['level'].upper())

		if not os.path.isdir(log_dir):
			os.mkdir(log_dir)

		logging.basicConfig(
			filename=log_file,
			format=config.LOGS['format'],
			level=log_level_no,
		)

	def enable_debug_console(self):
		"""Enable stderr logging, activate_logging must be called first."""
		log = logging.getLogger()
		stream_log = logging.StreamHandler()
		stream_formatter = logging.Formatter(config.LOGS['format'])
		stream_log.setLevel(logging.DEBUG)
		stream_log.setFormatter(stream_formatter)
		log.addHandler(stream_log)
