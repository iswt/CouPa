#!/usr/bin/env python
import sys
import os

from gui import CouPaGUI
from lib import get_parser, SimpleConfig, WalletConfig, setup_logging, runlog

if __name__ == '__main__':
	parser = get_parser()
	args = parser.parse_args()
	
	config = SimpleConfig(args.__dict__)
	setup_logging(config.get('logfile'))
	runlog.debug('CouPa directory is {}'.format(config.path))
	
	if config.get('wallet_path'):
		w = WalletConfig(config.get('wallet_path'))
	
	cmd = config.get('cmd')
	
	if cmd in ['gui']:
		CouPaGUI(config)
	
	sys.exit(0)