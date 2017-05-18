#!/usr/bin/env python
import sys, os
from decimal import Decimal

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
