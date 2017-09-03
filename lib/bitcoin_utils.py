#!/usr/bin/env python
import sys, os
import json
from decimal import Decimal

try:
	import bitcoin.rpc
	from bitcoin.core import b2x, b2lx, x, lx, str_money_value, COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint
	from bitcoin.core.script import CScript, OP_RETURN, OP_CHECKMULTISIG
	from bitcoin.wallet import CBitcoinAddress
except ImportError:
	print('Cannot import python-bitcoinlib, you can try installing it through pip with: pip install python-bitcoinlib')
	sys.exit(0)

from lib import runlog, get_config, AsyncAction

def rpc_request(callback, method, *args):
	config = get_config()
	url = config.get('btc_url')
	if not url:
		return None
	rpc = bitcoin.rpc.Proxy(service_url=url)
	AsyncAction(rpc._call, method, *args, callback=callback)
	
	return True

def get_utxos_for_address_async(address, callback):
	def cb(raw_transactions):
		inputs = []
		outputs = []
		full_outputs = {}
		utxos = []
		for i, tx in enumerate(raw_transactions):
			for vout in [x for x in tx['vout'] if 'scriptPubKey' in x and 'addresses' in x['scriptPubKey'] and addy in x['scriptPubKey']['addresses']]:
				outputs.append({'txid': tx['txid'], 'vout': vout['n']})
				full_outputs[(tx['txid'], vout['n'])] = vout
			for vin in tx['vin']:
				inputs.append({'txid': vin['txid'], 'vout': vin['vout']})
		
		utxos = [d for d in outputs if d not in inputs]
		utxos = [full_outputs[(d['txid'], d['vout'])] for d in utxos]
		
		if callback:
			callback(utxos, address)
	
	rpc_request(cb, 'searchrawtransactions', address, 1, 0, 999999)
