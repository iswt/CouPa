#!/usr/bin/env python
import sys, os
from decimal import Decimal
from threading import Thread

from lib import runlog

def to_satoshis(x):
	return int((Decimal(x) * Decimal(1e8)).quantize(Decimal('1.00000000')))

def from_satoshis(x):
	return (Decimal(x) / Decimal(1e8)).quantize(Decimal('1.00000000'))

def user_dir():
	if os.name == 'posix':
		return os.path.join(os.environ['HOME'], '.coupa')
	elif 'APPDATA' in os.environ:
		return os.path.join(os.environ['APPDATA'], 'CouPa')
	elif 'LOCALAPPDATA' in os.environ:
		return os.path.join(os.environ['LOCALAPPDATA'], 'CouPa')
	else:
		return None

class AsyncAction(Thread):
	def __init__(self, func, *args, **kwargs):
		super(AsyncAction, self).__init__(target=self.do_action)
		self.daemon = True
		self.action_func = func
		self.function_args = args
		self.callback = None
		if 'callback' in kwargs and kwargs['callback']:
			self.callback = kwargs['callback']
		self.passthrough_args = []
		if 'passthrough' in kwargs and kwargs['passthrough']:
			self.passthrough_args = kwargs['passthrough']
		
		self.start()
	
	def do_action(self):
		res = self.action_func(*self.function_args)
		if self.callback:
			self.callback(res, *self.passthrough_args)
	
