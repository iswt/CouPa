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

from .qt import CouPaWindow

class CouPaGUI:
	def __init__(self, config):
		self.config = config
		
		#self.efilter = OpenFileEventFilter(self.windows)
		self.app = QApplication(sys.argv)
		#self.app.installEventFilter(self.efilter)
		self.mw = CouPaWindow()
		self.mw.show()
		
		self.app.exec_()