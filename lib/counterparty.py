#!/usr/bin/env python
import sys, os
import json
from base64 import b64encode
from decimal import Decimal

from lib import runlog, get_config, AsyncRequest

asset_info = { # quick list of assets and their locked/divisible status
	'XCP': {'divisible': True, 'locked': True}, 'BITCRYSTALS': {'divisible': True, 'locked': True},
	'GEMZ': {'divisible': True, 'locked': True}, 'FLDC': {'divisible': True, 'locked': True},
	'PROTONEXIUM': {'divisible': True, 'locked': True}
}

def rpc_request(payload, callback, tojson=True):
	config = get_config()
	user = config.get('xcp_user')
	pw = config.get('xcp_pass')
	url = config.get('xcp_url')
	if not user or not pw or not url:
		runlog.error('You must set xcp_user, xcp_pass and xcp_url in your configuration file to make counterparty requests.')
		return None
	
	if url[-1] == '/': # strip trailing slash if it exists
		url = url[:-1]
	url = '{}/api/'.format(url)
	
	if 'jsonrpc' not in payload.keys():
		payload['jsonrpc'] = '2.0'
	if 'id' not in payload.keys():
		payload['id'] = 0
	
	def response_function(response):
		ret = {}
		if type(response) is not dict:	
			if tojson:
				response = json.loads(response)
				if 'error' in response.keys():
					runlog.error('Failed counterparty request: {}'.format(response['error']))
				else:
					ret = response['result']
			else:
				runlog.warn('Unexpected result from counterparty call: {}'.format(response))
		else:
			if 'result' in response:
				ret = response['result']
			else:
				ret = response
				
		callback(ret)
	
	AsyncRequest(
		'POST', url, json.dumps(payload), headers={
			'Authorization': 'Basic {}'.format(b64encode(bytes('{}:{}'.format(user, pw), 'utf-8')).decode('utf-8'))
		}, response_func=response_function,
		timeout=config.get('xcp_timeout', 10)
	)
