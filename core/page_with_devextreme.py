import os
import json
from ..config import setup as config
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
		connect_src = []

		if config.CONTENT_SECURITY_POLICY_CONNECT:
			connect_src.append(config.CONTENT_SECURITY_POLICY_CONNECT)

		self.html += '<!DOCTYPE html>'
		self.html += '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">'

		self.to_head("""<meta http-equiv="Content-Security-Policy" content="
						default-src 'self';
						style-src 'self' 'unsafe-inline';
						script-src 'self' 'unsafe-inline' 'unsafe-eval';
						connect-src 'self' %s;
						img-src 'self' data:;
					"/>""" % (" ".join(connect_src))
		)

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
		javascript_folder = "cause-web-content"
		template_folder = "cause-web-content"

		if os.path.isdir("%s/static/cause-web-javascript" % config.ROOT):
			javascript_folder = "cause-web-javascript"
		if os.path.isdir("%s/static/cause-web-template" % config.ROOT):
			template_folder = "cause-web-template"

		self.to_head('<link rel="icon" href="/static/%s/images/favicon.png">' % template_folder)
		self.to_head('<link rel="apple-touch-icon" href="/static/%s/images/logo.png" />' % template_folder)
		self.to_head('<link rel="dx-template" type="text/html" href="/static/%s/layouts/DesktopLayout.html" />' % template_folder)
		self.to_head('<link rel="stylesheet" type="text/css" href="/static/plugins/devExtreme/%s/css/dx.common.css" />' % config.VERSION["devExtreme"])
		self.to_head('<link rel="stylesheet" type="text/css" href="/static/plugins/devExtreme/%s/css/dx.spa.css" />' % config.VERSION["devExtreme"])
		self.to_head('<link rel="dx-theme" data-theme="generic.light" type="text/css" href="/static/%s/css/generic.light.custom-%s.css" />' % (
			template_folder,
			config.VERSION["devExtreme"][0:4],
		))
		self.to_head('<link rel="stylesheet" type="text/css" href="/static/%s/css/generic.cause.css" />' % template_folder)
		self.js(['/static/%s/js/cause%s.js' % (javascript_folder, "" if config.IS_DEV else ".min",)])

		self.add_config()

	def add_config(self):
		access = []

		if hasattr(config, "WEBSERVICE") and config.WEBSERVICE is not None and Session.get('access_token') is not None:
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
					if feature['access'] is True:
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
				'webservice': config.WEBSERVICE if hasattr(config, "WEBSERVICE") else "",
				'webroot': config.WEBROOT
			}))
		)

if __name__ == '__main__':
	PageWithDevextreme()
