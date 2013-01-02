import sys, pycurl
from cStringIO import StringIO

## PyGTK use to send url to clipboard
# Constants
OPT = {
	'PYGTK_MODULE'   : False,
	'VERBOSE_OUTPUT' : False
}

try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	OPT['PYGTK_MODULE'] = True
except:
	OPT['PYGTK_MODULE'] = False

def setopt(optname, value):
	OPT[optname] = value

def DBG(msg, code = 0):
	if OPT['VERBOSE_OUTPUT']:
		print {
			0: "INFO: %s" % msg,
			1: "WARN: %s" % msg,
			2: "Error: %s" % msg
		}[code]

class clipB:
	def __init__(self):
		self.cb = gtk.clipboard_get()
	def send_text(self, text):
		self.cb.set_text(text)
		self.cb.store()

def copyToClipB(text):
	if OPT['PYGTK_MODULE'] == False:
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
		if OPT['VERBOSE_OUTPUT']:
			self.cp.setopt(self.cp.VERBOSE, 1)
			self.cp.setopt(self.cp.DEBUGFUNCTION, self.debug)
		
		self.cp.perform()
		
		return result.getvalue()

	def debug(self, dtype, dmsg):
		sys.stdout.write("PycURL: (%d): %s" % (dtype, dmsg))