import sys, os
import json
import threading
from copy import deepcopy

from .util import user_dir

config_name = 'coupa.conf'

config = None
def get_config():
	global config
	return config
	
def set_config(newconf):
	global config
	config = newconf

class SimpleConfig(object):
	def __init__(self, cli_options={}, set_global_config=True):
		self.lock = threading.RLock()
		self.user_dir = user_dir
		self.configname = config_name
		
		self.cli_options = deepcopy(cli_options)
		self.user_config = {}
		self.system_config = {}
		
		self.path = self.coupa_path()
		self.user_config = read_user_config(self.path)
		
		if set_global_config:
			set_config(self)
	
	def coupa_path(self):
		# read coupa_path from command line / system configuration
		# otherwise use the default data directory for the user
		path = self.get('coupa_path')
		if path is None:
			path = self.user_dir()
		
		if not os.path.exists(path): # if the directory does not exist, create it
			if os.path.islink(path):
				raise Exception('Dangling link: {}'.format(path))
			os.mkdir(path)
		
		return path
	
	def get(self, key, default=None):
		with self.lock:
			out = self.cli_options.get(key)
			if out is None:
				out = self.user_config.get(key)
				if out is None:
					out = self.system_config.get(key, default)
		return out
	
	def set_key(self, key, value, save=True):
		with self.lock:
			self.user_config[key] = value
			if save:
				self.save_user_config()
	
	def save_user_config(self):
		if not self.path:
			return None
		path = os.path.join(self.path, self.configname)
		f = open(path, 'w')
		f.write(json.dumps(self.user_config, indent=2, sort_keys=True))
		f.close()
	
	def save(self):
		self.save_user_config()
		
	def config_exists(self):
		if os.path.isfile(os.path.join(self.path, self.configname)):
			return True
		return False
	
def read_user_config(path, name=None):
	if not path:
		return {}
	if not name:
		name = config_name
	
	config_path = os.path.join(path, name)
	if not os.path.exists(config_path):
		return {}
	try:
		with open(config_path, 'r') as f:
			data = f.read()
			result = json.loads(data)
	except:
		print('Cannot read config file: {}'.format(config_path))
		return {}
	if type(result) is not dict:
		return {}
	return result
