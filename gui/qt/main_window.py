#!/usr/bin/env python
import os, sys
import time, json

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore

from lib import counterparty, runlog
from lib.util import to_satoshis, from_satoshis

class HistoryTableWidget(QTableWidget):
	
	# use object when a dictionary will be emitted through the signal
	# http://stackoverflow.com/questions/43964766/pyqt-emit-signal-with-dict/43977161#43977161
	new_item_sig = QtCore.pyqtSignal(object)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setShowGrid(False)
		
		self.header = self.horizontalHeader()
		self.vertical_header = self.verticalHeader()
		self.vertical_header.hide()
		
		self.history = []
		
		self.setColumnCount(5)
		self.update_labels()
		
		self.new_item_sig.connect(self.on_new_item)
		
	def update_labels(self):
		self.setHorizontalHeaderLabels(['#', 'Block', 'Date', 'Asset', 'Address'])
		self.header.setDefaultAlignment(Qt.AlignHCenter)
		
		self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(3, QHeaderView.Stretch)
		self.header.setSectionResizeMode(4, QHeaderView.Stretch)
	
	def populate_from_info(self, infod):
		self.setColumnCount(4)
		self.setRowCount(3)
		
		self.update_labels()
		
	@QtCore.pyqtSlot(object)
	def on_new_item(self, response):
		addy = '1MXMayerNuiCjT5VobxFhwnwJCLW4UMFRA'
		for i, d in enumerate(sorted(response, key=lambda x: x['block_index'])):
			if d['asset'] in counterparty.asset_info and counterparty.asset_info[d['asset']]['divisible']:
				d['quantity'] = str(from_satoshis(d['quantity'])).rstrip('0').rstrip('.')
			txmsg = '  '
			showaddy = d['source']
			if d['source'] == addy:
				txmsg = '- '
				showaddy = d['destination']
			txmsg += '{} {}'.format(d['quantity'], d['asset'])
			row = [
				{'column': 0, 'item': QTableWidgetItem('{}'.format(i + 1))},
				{'column': 1, 'item': QTableWidgetItem('{}'.format(d['block_index']))},
				{'column': 2, 'item': QTableWidgetItem('xxx')},
				{'column': 3, 'item': QTableWidgetItem(txmsg)},
				{'column': 4, 'item': QTableWidgetItem(showaddy)}
			]
			if '-' in txmsg:
				for r in row:
					r['item'].setForeground(QColor(225, 86, 86))
			
			self.add_new(row)
		
	def add_new(self, columns_info):		
		self.insertRow(0)
		for d in columns_info:
			self.setItem(0, d['column'], d['item'])
		
		self.sortItems(1, Qt.DescendingOrder)
		rowcount = self.rowCount()
		for rownum in range(rowcount): # set the # column correctly 
			self.setItem(rownum, 0, QTableWidgetItem('{}'.format(rowcount - (rownum + 1))))
			
	def populate_from_counterparty(self):
		addy = '1MXMayerNuiCjT5VobxFhwnwJCLW4UMFRA'
		payload = {
			'method': 'get_sends', 'params': {
				'filters': [
					{'field': 'destination', 'op': '==', 'value': addy}
				]
			}
		}
		
		def cb(response):
			self.new_item_sig.emit(response)
		
		creds = counterparty.rpc_request(payload, cb)
		payload['params']['filters'][0]['field'] = 'source'
		debits = counterparty.rpc_request(payload, cb)
	
class MainWidget(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.layout = QGridLayout(self)
		
		self.create_history_tab()
		
		self.setLayout(self.layout)
		
	def create_history_tab(self):
		self.history_table = HistoryTableWidget()
		self.layout.addWidget(self.history_table)
		
		self.history_table.populate_from_counterparty()

class CouPaWindow(QMainWindow):
	
	def __init__(self):
		super().__init__()
		
		self.init_ui()
		
	def init_ui(self):
		self.setGeometry(350, 350, 768, 512)
		self.setWindowTitle('CouPa')
		
		#self.statusBar().showMessage('Ready')
		self.setup_menubar()
		self.setup_toolbar()
		
		self.mw = MainWidget(self) 
		self.setCentralWidget(self.mw)

	def setup_toolbar(self):
		left_spacer = QWidget()
		left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		right_spacer = QWidget()
		right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		self.status_label = QLabel('Not Connected')
		
		prefAction = QAction(QIcon('icons/preferences.png'), '&Preferences', self)
		prefAction.setStatusTip('Preferences')
		
		self.main_toolbar = QToolBar()
		self.main_toolbar.setMovable(False)
		self.main_toolbar.addWidget(self.status_label)
		self.main_toolbar.addWidget(left_spacer)
		self.main_toolbar.addAction(prefAction)
		#self.main_toolbar.addWidget(right_spacer)
		self.addToolBar(Qt.BottomToolBarArea, self.main_toolbar)
		

	def setup_menubar(self):
		self.menubar = self.menuBar()
		
		exitAction = QAction(QIcon('exit.png'), '&Quit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit CouPa')
		exitAction.triggered.connect(qApp.quit)
		
		fileMenu = self.menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		# -----------------------------------------------------------
		xpubAction = QAction(QIcon('xpubkey.png'), '&Show xpubkey', self)
		xpubAction.setStatusTip('Show the current seeds xpubkey')
		
		toolMenu = self.menubar.addMenu('&Seed')
		toolMenu.addAction(xpubAction)
		# -----------------------------------------------------------
		aboutAction = QAction(QIcon('help.png'), '&About', self)
		aboutAction.setStatusTip('About CouPa')
		
		helpMenu = self.menubar.addMenu('&Help')
		helpMenu.addAction(aboutAction)
		
		