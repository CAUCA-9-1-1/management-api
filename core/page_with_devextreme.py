import json
from ..config import setup as config
from ..resturls.permissionwebuser import PermissionWebuser
from .session import Session
from .request import Request


class PageWithDevextreme:
	""" Crée une page HTML
	"""
	html = ""
	head = """
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		"""
	body = "<noscript>Your browser doesn\'t support JavaScript or it\'s disable.</noscript>"

	def __init__(self):
		""" Place the HTML5 doctype
		"""
		connect_src = [config.CAUSEJS]

		if config.CONTENT_SECURITY_POLICY_CONNECT:
			connect_src.append(config.CONTENT_SECURITY_POLICY_CONNECT)

		if config.WEBSERVICE is not None:
			connect_src.append(config.WEBSERVICE['host'])

		self.html += '<!DOCTYPE html>'
		self.html += '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">'

		self.to_head("""<meta http-equiv="Content-Security-Policy" content="
						default-src 'self' %s;
						style-src 'self' %s 'unsafe-inline';
						script-src 'self' %s 'unsafe-inline' 'unsafe-eval';
						connect-src 'self' %s;
						img-src 'self' %s data:;
					"/>""" % (
			config.CAUSEJS, config.CAUSEJS, config.CAUSEJS, " ".join(connect_src), config.CAUSEJS
		))

	def show(self):
		""" Return the complete page

		:return: Complete HTML page
		"""
		self.html += '<head>' + self.head + '</head><body>' + self.body + '</body></html>'

		return self.html

	def title(self, title):
		""" Set the page title tag

		:param title: Page title
		"""
		self.head += '<title>' + title + '</title>'

	def css(self, file):
		""" Add a stylesheet file on page

		:param file: CSS url
		"""
		for f in file:
			if isinstance(f, dict):
				self.to_head('<link ' + ' '.join(['%s="%s"' % (key, value) for (key, value) in f.items()]) + ' />')
			else:
				self.to_head('<link rel="stylesheet" type="text/css" href="' + f + '" />')

	def js(self, file):
		""" Add a Javascript file on page

		:param file: JS file
		"""
		for f in file:
			self.to_head('<script type="text/javascript" src="' + f + '"></script>')

	def to_head(self, tag):
		""" Add a generic html tag to the head

		:param tag: HTML tag
		"""
		self.head += tag

	def to_body(self, tag):
		""" Add a generic html tag to the body

		:param tag: HTML tag
		"""
		self.body += tag

	def add_cause(self):
		folder = '//%s/' % config.CAUSEJS
		if config.MINIMIZE_JS is False:
			folder = '/causeJs/'

		if config.MINIMIZE_JS is True:
			self.js([folder + 'cause/js/cause%s.js' % ("" if config.IS_DEV else ".min")])
		else:
			self.js(['/js/'])

		self.to_head('<link rel="icon" href="' + folder + 'cause/images/favicon.png">')
		self.add_config()

	def add_config(self):
		access = []
		version = 'DEV' if config.PACKAGE_VERSION == '__package_version__' else config.PACKAGE_VERSION

		if config.WEBSERVICE is not None and Session.get('access_token') is not None:
			config.WEBSERVICE.update({
				'access_token': Session.get('access_token'),
				'refresh_token': Session.get('refresh_token')
			})

			query = Request("%s/permissionwebuser/%s" % (config.WEBSERVICE['host'], Session.get('id_webuser')), 'GET')
			permission = json.loads(query.send(None, None, {
				'Authorization': 'Token %s' % config.WEBSERVICE['access_token']
			}))

			if permission is not None and 'data' in permission and permission['data'] is not None:
				for feature in permission['data']:
					access.append(feature['feature_name'])

		self.to_head("""
				<script>
					cause.version = cause.extend({}, cause.version, %s);
					window.myApp = {
						model: {},
						access: %s,
						config: cause.extend({}, %s)
					};
				</script>
			""" % (
			json.dumps(config.VERSION),
			json.dumps(access),
			json.dumps({
				'version': config.PACKAGE_VERSION,
				'isdev': config.IS_DEV,
				'webservice': config.WEBSERVICE,
				'webroot': config.WEBROOT
			}))
		)

	def add_dev_extreme(self):
		folder = '//%s/' % config.CAUSEJS
		if config.MINIMIZE_JS is False:
			folder = '/causeJs/'

		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Simple/SimpleLayout.html"/>')
		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Popup/PopupLayout.html"/>')
		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/SlideOut/SlideOutLayout.html"/>')
		self.css([
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/css/dx.common.css',
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/css/dx.spa.css',
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Simple/SimpleLayout.css',
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Popup/PopupLayout.css',
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/SlideOut/SlideOutLayout.css',
				folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Desktop/DesktopLayout.css',
				{'rel': 'dx-theme', 'data-theme': 'generic.light', 'href': folder + 'cause/css/generic.light.custom-%s.css' % config.VERSION['devExtreme']}])

		if config.VERSION['devExtreme'] == '16.2.4' or config.VERSION['devExtreme'] == '16.2.6':
			self.includeDevExtreme16_2(folder)
		elif config.VERSION['devExtreme'] == '16.1.7' or config.VERSION['devExtreme'] == '16.1.8':
			self.includeDevExtreme16_1(folder)
		else:
			self.includeDevExtreme15(folder)

	def includeDevExtreme16_2(self, folder):
		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/layouts/DesktopLayout.html"/>')
		self.js([
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/jquery-' + config.VERSION['jQuery'] + '.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/knockout-3.4.0.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/jszip.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr/event.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr/supplemental.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/message.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/number.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/date.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/currency.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/dx.messages.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/localization/dx.web.fr.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Simple/SimpleLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Popup/PopupLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/SlideOut/SlideOutLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Desktop/DesktopLayout.js'])

	def includeDevExtreme16_1(self, folder):
		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/layouts/DesktopLayout.html"/>')
		self.js([
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/jquery-2.2.3.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/knockout-3.4.0.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/jszip.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr/event.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/cldr/supplemental.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/message.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/number.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/date.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize/currency.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/dx.all.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/localization/dx.all.fr.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Simple/SimpleLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Popup/PopupLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/SlideOut/SlideOutLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Desktop/DesktopLayout.js'])

	def includeDevExtreme15(self, folder):
		self.to_head('<link rel="dx-template" type="text/html" href="' + folder + 'cause/layouts/DesktopLayout.html"/>')
		self.js([
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/jquery-2.1.4.min.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/knockout-3.4.0.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/globalize.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/dx.all.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/js/localization/dx.all.fr.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Simple/SimpleLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Popup/PopupLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/SlideOut/SlideOutLayout.js',
			folder + 'cause/plugins/devExtreme/' + config.VERSION['devExtreme'] + '/layouts/Desktop/DesktopLayout.js'])

if __name__ == '__main__':
	PageWithDevextreme()
