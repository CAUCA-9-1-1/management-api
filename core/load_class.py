import os
import importlib.util
from ..config import setup as config


class LoadClass:
	def load_class(self, name):
		class_object = None

		for folder in config.SEARCH_FOLDERS:
			class_object = self.load_class_from(folder, name)

			if class_object is not None:
				break

		if class_object is None:
			raise Exception("We can't find the class: %s" % name)
		else:
			return class_object

	def load_class_from(self, folder, class_name):
		file_name = "%s.resturls.%s" % (folder, class_name.lower())
		file = '%s/%s.py' % (config.ROOT, file_name.replace('.', '/'))

		if not os.path.isfile(file) and folder[0:5] == 'cause':
			file = '%s/%s.py' % (config.ROOT[0:config.ROOT.rfind('/')], file_name.replace('.', '/'))

		if not os.path.isfile(file):
			return None

		try:
			module_loaded = importlib.import_module(file_name, '%s.resturls' % folder)
			class_object = getattr(module_loaded, class_name)

			return class_object
		except Exception as e:
			raise Exception("Loading exception on class '%s': %s" % (class_name, e))