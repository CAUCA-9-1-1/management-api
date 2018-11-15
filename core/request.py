import ssl
import logging
import urllib.parse
import urllib.request
from .exceptions import RequestException


class Request:
    url = ''
    method = 'POST'

    def __init__(self, url='', method='POST'):
        self.url = url
        self.method = method

    def send(self, data, url=None, headers=None):
        if url is not None:
            self.url = url

        if data is None:
            data = ''
        else:
            data = urllib.parse.urlencode(data)

        if self.method == 'GET':
            request = urllib.request.Request(self.url + ('?' if data else '') + data, method=self.method)
        else:
            request = urllib.request.Request(self.url, data.encode('ascii'), method=self.method)

        if headers is not None:
            for key in headers:
                request.add_header(key, headers[key])

        logging.info('Url = %s, Data = %s, Method = %s', self.url, data, self.method)

        if "https://" in self.url:
            return self.send_https(request)
        return self.send_http(request)

    def send_https(self, request):
        try:
            context = ssl._create_unverified_context()

            with urllib.request.urlopen(request, context=context) as response:
                html = self.read_request(response)
        except urllib.error.HTTPError as e:
            logging.info('Url: %s, Response: %s', self.url, e)
            raise RequestException("Error during request, we can't access to %s" % self.url)
        except urllib.error.URLError as e:
            logging.info('Url: %s, Response: %s', self.url, e)
            raise RequestException("URL error, we can't access to %s" % self.url)

        return html or '{}'

    def send_http(self, request):
        try:
            with urllib.request.urlopen(request) as response:
                html = self.read_request(response)
        except urllib.error.HTTPError as e:
            logging.info('Url: %s, Response: %s', self.url, e)
            raise RequestException("Error during request, we can't access to %s" % self.url)
        except urllib.error.URLError as e:
            logging.info('Url: %s, Response: %s', self.url, e)
            raise RequestException("URL error, we can't access to %s" % self.url)

        return html or '{}'

    def read_request(self, response):
        if response.status == 200:
            raw = response.read()
            html = raw.decode('utf-8')
            logging.info('Response = %s', raw)
        else:
            raise RequestException('Response.status = %s' % str(response.status))

        return html or None