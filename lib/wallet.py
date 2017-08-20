#!/usr/bin/env python
import sys
import os
import json

from lib import runlog, SimpleConfig, read_user_config, CounterpartyMnemonic
from .util import AsyncAction

def generate_addresses(seed, seed_type, x, y, hardened=True):
	addresses = []
	if seed_type.lower() in ['counterparty']:
		cm = CounterpartyMnemonic()
		k = cm.from_phrase(seed)
		for i in range(x, y):
			a = cm.get_address_at(k, i, harden=hardened)
			addresses.append( {
				'address': a.Address()
			} )
	
	return addresses

class WalletConfig(SimpleConfig):
	def __init__(self, filename):
		super(WalletConfig, self).__init__(set_global_config=False)
		
		self.configname = filename
		self.path = self.wallet_path()
		
		self.user_config = read_user_config(self.path, self.configname)
	
	def wallet_path(self):
		path = os.path.join(self.path, 'wallets')
		if not os.path.exists(path): # if the directory does not exist, create it
			if os.path.islink(path):
				raise Exception('Dangling link: {}'.format(path))
			os.mkdir(path)
		return path
	
	def generate_initial_addresses(self, seed, initial_count, callback=None):
		hardened = self.get('hardened', True)
		seed_type = self.get('seed_type', None)
		if not seed_type:
			return None
		if self.get('addresses') is not None: # don't overwrite addresses
			return None
		
		def cb(addresses):
			self.set_key('addresses', addresses)
			runlog.info('Generated addresses {}'.format(addresses))
			if callback:
				callback(addresses)
		
		AsyncAction(generate_addresses, seed, seed_type, 0, initial_count, hardened, callback=cb)
	
