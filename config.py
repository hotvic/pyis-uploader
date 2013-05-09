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

class O(object):
	def __init__(self):
		self.opts = DEFAULTS
	def getopt(self, optname):
		return self.opts[optname]
	def getopts(self):
		return self.opts
	def setopt(self, optname, value = None):
		self.opts[optname] = value
	def save(self):
		pass

class Config(object):
    def __init__(self):
        """ Create a new 'Config' object """
        self._tempdict = {}
        self._cfile = None
        self._opts = DEFAULTS

    def _load(self):
        """ Private function for load config file """
        cfgdir = os.getenv('XDG_CONFIG_HOME', os.getenv('HOME') + '/.config') + '/pyis-uploader'
        cfgfile = cfgdir + '/config.json'
        if os.path.ifdir(cfgdir) and os.path.isfile(cfgfile):
            self._cfile = open(cfgfile, 'rw')
        else os.path.exists(cfgdit) and os.path.isdir(cfgdir):
            self._cfile = open(cfgfile, 'w')
        elif not os.path.exits(cfgdir):
            os.mkdir(cfgdir)

    def _parsejson(self):
        """ Private function for manipulate and parse json (read-only) """
        pass

    def _writejson(se lf):
        """ Private function for manipulate and dumps json (write-only) """
        pass

    def getopt(self, opt):
        """ Return an option value """
        pass
 
    def setopt(self, opt, value):
        """ Set an option value (doesn't write yet!) """
        pass

    def getopt_all(self):
        """ Return all options and respectively values """
        pass
