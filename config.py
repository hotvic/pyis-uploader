# -*- coding: UTF-8 -*-
# 
# Copyright © 2012, 2013 Victor Aurélio <victoraur.santos@gmail.com>
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

import os
import json

DEFAULTS = {
    'IMAGESHACK_KEY'  : "47DHIJMSe847793024d16f9db3e6f7b0d31389cc",
	'ONLY_PRINT_URL'  : False,
	'ONLY_PRINT_THB'  : False,
    'PRINT_FULL_IN_M' : False,
	'SEND_CLIPBOARD'  : False,
	'RESIZE_IMAGE'    : False,
	'USER_USER'       : False,
	'USER_PASSWORD'   : False,
	'USER_COOKIE'     : False,
    'IMAGE_TAGS'      : False,
	'PYGTK_MODULE'    : False,
	'VERBOSE_OUTPUT'  : False
}

class FBConfig(object):
	def __init__(self):
		self.opts = DEFAULTS
	def getopt(self, optname):
		return self.opts[optname]
	def getopt_all(self):
		return self.opts
	def setopt(self, optname, value = None):
		self.opts[optname] = value
	def close(self):
		pass

class PConfig(object):
    def __init__(self):
        """ Create a new 'Config' object """
        self._tempdict = {}
        self._cfile = None
        self._opts = DEFAULTS
        self._load()
        self._parsejson()

    def _load(self):
        """ Private function for load config file """
        self.cfgdir = os.getenv('XDG_CONFIG_HOME', os.getenv('HOME') + '/.config') + '/pyis-uploader'
        self.cfgfile = self.cfgdir + '/config.json'
        if os.path.isdir(self.cfgdir) and os.path.isfile(self.cfgfile):
            with open(self.cfgfile, 'r') as f:
                self._cfile = f.read()
        elif not os.path.exists(self.cfgdir):
            os.mkdir(self.cfgdir)

    def _parsejson(self):
        """ Private function for manipulate and parse json (read-only) """
        if self._cfile == None:
            self._tempdict = self._opts
        else:
            self._tempdict = json.loads(self._cfile)

    def _writejson(self):
        """ Private function for manipulate and dumps json (write-only) """
        with open(self.cfgfile, 'w') as f:
            dump = json.dumps(self._tempdict, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(dump)

    def getopt(self, opt):
        """ Return an option value """
        if opt in self._tempdict:
            return self._tempdict[opt]
        elif not opt in self._tempdict and opt in self._opts:
            return self._opts[opt]
        else:
            return False
 
    def setopt(self, opt, value):
        """ Set an option value (doesn't write yet!) """
        if opt in self._opts:
            self._tempdict[opt] = value
        else:
            return False

    def getopt_all(self):
        """ Return all options and respectively values """
        return self._tempdict

    def close(self):
        """ Write changes to configuration file """
        self._writejson()

def Config():
    if os.name == "posix":
        return PConfig()
    else:
        return FBConfig()
