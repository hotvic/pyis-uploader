# -*- coding: UTF-8 -*-
# 
# Copyright © 2013 Victor Aurélio <victoraur.santos@gmail.com>
#
# This file is part of PyIS-Uploader.
#
# PyIS-Uploader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyIS-Uploader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from progressbar import *
from cStringIO import StringIO

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
