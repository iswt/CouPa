import sys, os
import argparse

def set_default_subparser(self, name, args=None):
	'''
	see http://stackoverflow.com/questions/5176691/argparse-how-to-specify-a-default-subcommand
	'''
	subparser_found = False
	help_found = False
	for arg in sys.argv[1:]:
		if arg in ['-h', '--help']:  # global help if no subparser
			help_found = True
			break
		else:
			for x in self._subparsers._actions:
				if not isinstance(x, argparse._SubParsersAction):
					continue
				for sp_name in x._name_parser_map.keys():
					if sp_name in sys.argv[1:]:
						subparser_found = True
	if not subparser_found and not help_found:
		# insert default in first position, this implies no
		# global options without a sub_parsers specified
		if args is None:
			sys.argv.insert(1, name)
		else:
			args.insert(0, name)
argparse.ArgumentParser.set_default_subparser = set_default_subparser

def add_global_options(parser):
	opts = parser.add_argument_group('global options')
	opts.add_argument('-D', '--dir', dest='coupa_path', help='CouPa directory')

def get_parser():
	parser = argparse.ArgumentParser(
		description='CouPa',
		epilog='Run "coupa <command> -h" to see specific command help'
	)
	add_global_options(parser)
	
	subparsers = parser.add_subparsers(dest='cmd', metavar='<command>')
	# gui
	parser_gui = subparsers.add_parser(
		'gui', description='Run the CouPa Graphical User Interface.', help='Run GUI (default)'
	)
	parser_gui.add_argument(
		'-g', '--gui', dest='gui',
		help='select graphical user interface', choices=['qt']
	)
	add_global_options(parser_gui)
	
	parser.set_default_subparser('gui') # default command
	return parser
	