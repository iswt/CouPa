import os, sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore

from lib import runlog, WalletConfig

class NameOptions(QWizardPage):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.layout = QVBoxLayout()
		self.init_ui()
		self.setLayout(self.layout)
	
	def init_ui(self):
		self.walletname = QLineEdit(self)
		self.walletlabel = QLabel('Wallet Name')
		self.layout.addWidget(self.walletlabel)
		self.layout.addWidget(self.walletname)
		
		self.registerField('walletname*', self.walletname)

class WalletTypeOptions(QWizardPage):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		
		self.layout = QVBoxLayout()
		self.init_ui()
		self.setLayout(self.layout)
		
	def init_ui(self):
		self.label = QLabel('Seed type')
		self.layout.addWidget(self.label)
		
		self.seedcombo = QComboBox(self)
		self.seedcombo.addItem('Counterparty')
		self.layout.addWidget(self.seedcombo)
		
		self.seedentry = QLineEdit(self)
		self.seedlabel = QLabel('Seed Phrase')
		self.layout.addWidget(self.seedlabel)
		self.layout.addWidget(self.seedentry)
		
		self.hardened = QCheckBox('Use hardened derivation')
		self.hardened.setChecked(True)
		self.layout.addWidget(self.hardened)
			
		self.registerField('seedcombo', self.seedcombo)
		self.registerField('seedentry*', self.seedentry)
		self.registerField('hardened', self.hardened)
		
	def initializePage(self):
		wn = self.parent.field('walletname')
		self.label.setText('Seed type for <b>{}</b>'.format(wn))
		

class ConnectionOptions(QWizardPage):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		
		self.layout = QVBoxLayout()
		self.init_ui()
		self.setLayout(self.layout)
		
	def init_ui(self):
		self.label = QLabel('Enter connection details. This information can be entered or changed later on.')
		self.layout.addWidget(self.label)
		
		self.btcchk = QCheckBox('Bitcoin')
		self.btcchk.stateChanged.connect(lambda state: self.btcinfo.setEnabled(state))
		self.layout.addWidget(self.btcchk)
		
		hbox = QHBoxLayout()
		vb = QVBoxLayout()
		self.btcinfo = QLineEdit(self)
		self.btcinfo.setEnabled(False)
		self.btclabel = QLabel('Bitcoin url (e.g. http://rpcuser:rpcpassword@127.0.0.1:8332)')
		self.btclabel.setAlignment(Qt.AlignCenter)
		vb.addWidget(self.btclabel)
		vb.addWidget(self.btcinfo)
		hbox.addLayout(vb)
		self.layout.addLayout(hbox)
		
		self.cpchk = QCheckBox('Counterparty')
		self.cpchk.stateChanged.connect(self.on_cpchk_change)
		self.layout.addWidget(self.cpchk)
		
		cp_hbox = QHBoxLayout()
		cp_vb = QVBoxLayout()
		self.cpinfo = QLineEdit(self)
		self.cpinfo.setEnabled(False)
		self.cplabel = QLabel('Counterparty url (e.g. http://127.0.0.1:4000)')
		self.cplabel.setAlignment(Qt.AlignCenter)
		
		self.cp_user_info = QLineEdit(self)
		self.cp_user_info.setEnabled(False)
		self.cp_user_label = QLabel('Counterparty username')
		self.cp_user_label.setAlignment(Qt.AlignCenter)
		
		self.cp_pw_info = QLineEdit(self)
		self.cp_pw_info.setEnabled(False)
		self.cp_pw_label = QLabel('Counterparty password')
		self.cp_pw_label.setAlignment(Qt.AlignCenter)
		
		cp_vb.addWidget(self.cplabel)
		cp_vb.addWidget(self.cpinfo)
		cp_vb.addWidget(self.cp_user_label)
		cp_vb.addWidget(self.cp_user_info)
		cp_vb.addWidget(self.cp_pw_label)
		cp_vb.addWidget(self.cp_pw_info)
		
		cp_hbox.addLayout(cp_vb)
		self.layout.addLayout(cp_hbox)
		
		self.registerField('bitcoin_url', self.btcinfo)
		self.registerField('xcp_url', self.cpinfo)
		self.registerField('xcp_user', self.cp_user_info)
		self.registerField('xcp_password', self.cp_pw_info)
		
	def on_cpchk_change(self, state):
		self.cpinfo.setEnabled(state)
		self.cp_user_info.setEnabled(state)
		self.cp_pw_info.setEnabled(state)

class InitializationWizard(QWizard):
	def __init__(self, config, main_window=None, parent=None):
		super().__init__(parent)
		self.config = config
		self.main_window = main_window
		
		self.addPage(NameOptions(self))
		self.wto = WalletTypeOptions(self)
		self.addPage(self.wto)
		self.addPage(ConnectionOptions(self))
		
		self.setGeometry(350, 350, 768, 512)
		self.setWindowTitle('CouPa Initialization Wizard')
		
		finish = self.button(QWizard.FinishButton)
		finish.clicked.connect(self.on_finish)
	
	def on_finish(self):
		walletname = self.field('walletname')
		seed = self.field('seedentry')
		seed_type = self.wto.seedcombo.itemText(self.field('seedcombo'))
		hardened = self.field('hardened')
		
		self.config.set_key('btc_url', self.field('bitcoin_url'), False)
		self.config.set_key('xcp_url', self.field('xcp_url'), False)
		self.config.set_key('xcp_user', self.field('xcp_user'), False)
		self.config.set_key('xcp_pass', self.field('xcp_password'), False)
		self.config.save()
		
		wc = WalletConfig(walletname)
		wc.set_key('seed_type', seed_type, False)
		wc.set_key('hardened', hardened, False)
		wc.save()
		
		if self.main_window:
			self.main_window.show()
		
		# generate initial addresses
		mb = QMessageBox(self.main_window)
		mb.setWindowTitle('Generating addresses ...')
		mb.setText('Generating your addresses')
		mb.setStandardButtons(QMessageBox.NoButton)
		mb.setModal(False)
		mb.show()
		
		wc.generate_initial_addresses(seed, self.config.get('initial_address_generation_count', 10), lambda res: mb.accept())
		
