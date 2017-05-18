import sys, os
import time, datetime
from threading import Lock, Thread
try:
	import urllib.parse as urlparse
except ImportError:
	import urlparse
try:
	import http.client as httplib
except ImportError:
	import httplib

from lib import config, runlog

class AsyncRequest(Thread):
	def __init__(self, request_type, url, paramdata, timeout=3, parent=None, response_func=None, headers=None):
		self.parent = parent
		super(AsyncRequest, self).__init__(target=self.make_request)
		self.daemon = True
		self.url = urlparse.urlparse(url)
		self.timeout = timeout
		self.paramdata = paramdata
		self.request_type = request_type
		self.response_func = response_func
		self.headers = {
			'Host': self.url.hostname, 'Content-type': 'application/json',
			'User-Agent': 'CouPa'
		}
		if headers:
			for k, v in headers.items():
				self.headers[k] = v
		
		self.start()
	
	def make_request(self):
		try:
			conn = httplib.HTTPConnection(self.url.hostname, self.url.port, timeout=self.timeout)
			conn.request(
				self.request_type, self.url.path, self.paramdata, self.headers
			)
			resp = conn.getresponse().read().decode('utf-8')
			if self.response_func:
				resp = self.response_func(resp)
		except:
			runlog.exception('Failed request to {} on port {}'.format(self.url.hostname, self.url.port))
	