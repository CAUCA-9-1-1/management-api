import logging
import urllib.parse
import urllib.request


class Request:
	url = ''
	method = 'POST'

	def __init__(self, url='', method='POST'):
		self.url = url
		self.method = method

	def send(self, data, url=None, headers=None):
		html = ''

		if url is not None:
			self.url = url

		try:
			if data is None:
				data = ''
			else:
				data = urllib.parse.urlencode(data)

			if self.method == 'GET':
				request = urllib.request.Request(self.url + ('?' if data else '') + data, method=self.method)
			else:
				#data = data.replace('+', '%20')
				request = urllib.request.Request(self.url, data.encode('ascii'), method=self.method)

			if headers is not None:
				for key in headers:
					request.add_header(key, headers[key])

			with urllib.request.urlopen(request) as response:
				logging.info('Url = %s, Method = %s, Data = %s' % (self.url, self.method, str(data)))

				if response.status == 200:
					html = response.read().decode('UTF-8')

					logging.info('Response = %s' % html)
				else:
					logging.exception('Response.status = %s' % str(response.status))
		except Exception as e:
			logging.exception("Error during request")

		return html
