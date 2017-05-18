import sys
import logging
from logging.handlers import RotatingFileHandler
runlog = logging.getLogger('CouPa')

def setup_logging(filename=None):
	global runlog
	if filename:
		shandler = logging.RotatingFileHandler(filename, maxBytes=1024*1024*10, backupCount=256)
	else:
		shandler = logging.StreamHandler(sys.stdout)
	runlog.addHandler(shandler)
	shandler.setFormatter(
		logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', '%Y/%m/%d %H:%M:%S')
	)
	runlog.setLevel(logging.DEBUG)

from .config import SimpleConfig, get_config
from .cli import get_parser
from .network import AsyncRequest