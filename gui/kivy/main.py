#!/usr/bin/env python
import sys
import os

import kivy
kivy.require('1.0.7')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty, ListProperty

class MainPanel(TabbedPanel):	
	def print_wd(self):
		for widget in self.walk():
			print("[]->{}".format(widget, widget.id))
	
	def on_current_tab(self, b, c):
		print(self.current_tab)

class CouPaWindow(App):
	
	def init_ui(self):
		self.screens = {}
		
		self.history_screen = None
	
	def build(self):
		self.title = 'BIP32 Helper'
		#return Builder.load_file('main.kv')
		return MainPanel()
	
	def on_start(self):
		'''
		Kivy UI start point
		'''
		self.init_ui()
	
	def on_pause(self):
		return True
	
	def on_resume(self):
		pass
	
	
if __name__ == '__main__':
    CouPaWindow().run()