#!/usr/bin/env python
import sys, os
try:
    import PyQt5
except Exception:
    sys.exit('Error: Could not import PyQt5. You can try installing it with "pip install pyqt5"')

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore

from .qt import CouPaWindow, InitializationWizard

class CouPaGUI:
	def __init__(self, config):
		self.config = config
		
		#self.efilter = OpenFileEventFilter(self.windows)
		self.app = QApplication(sys.argv)
		#self.app.installEventFilter(self.efilter)
		
		self.cw = CouPaWindow()
		#self.cw.show()
		
		if self.config.config_exists():
			self.cw.show()
		else:
			self.launch_wizard()
		
		self.app.exec_()
		
	def launch_wizard(self):
		self.mw = InitializationWizard(self.config, self.cw);
		self.mw.show()
	