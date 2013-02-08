import sys
from progressbar import *
from cStringIO import StringIO

## 
#* This file is part of PyIS-Upload, licensed
#* under GNU GPL at version 3 or any other version.
##

## PyGTK use to send url to clipboard
try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	o.setopt('PYGTK_MODULE', True)
except:
	o.setopt('PYGTK_MODULE', False)

class clipB:
	def __init__(self):
		self.cb = gtk.clipboard_get()
	def send_text(self, text):
		self.cb.set_text(text)
		self.cb.store()

def copyToClipB(text):
	if not o.getopt('PYGTK_MODULE'):
		return False
	else:
		cb = clipB()
		cb.send_text(text)
		return True
