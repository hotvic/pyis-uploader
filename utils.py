import sys, pycurl
from cStringIO import StringIO

## PyGTK use to send url to clipboard
# Constants
PYGTK_MODULE   = False

try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	PYGTK_MODULE = True
except:
	PYGTK_MODULE = False

class clipB:
	def __init__(self):
		self.cb = gtk.clipboard_get()
	def send_text(self, text):
		self.cb.set_text(text)
		self.cb.store()

def copyToClipB(text):
	if PYGTK_MODULE == False:
		return False
	else:
		cb = clipB()
		cb.send_text(text)
		return True

## cURL class
class cURL:
	def __init__(self, url):
		self.URL = url
		self.cp = pycurl.Curl()

	def progress(self, dt, dd, ut, ud):
		percent = ut / 100;
		current = (ud != 0) and int(ud / percent) or 1
		sys.stdout.write("\r%d%%" % current)
		sys.stdout.flush()

	def getXML(self, POST):
		self.cp.setopt(self.cp.POST, 1)
		self.cp.setopt(self.cp.HTTPPOST, POST)
		self.cp.setopt(self.cp.URL, self.URL)

		#header = StringIO()
		#self.cp.setopt(self.cp.HEADERFUNCTION, header.write)
		
		result = StringIO()
		self.cp.setopt(self.cp.WRITEFUNCTION, result.write)
		self.cp.setopt(self.cp.NOPROGRESS, 0)
		self.cp.setopt(self.cp.PROGRESSFUNCTION, self.progress)
		
		self.cp.perform()
		
		return result.getvalue()