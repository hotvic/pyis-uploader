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

import os, sys, pycurl, json
from StringIO import StringIO
from HTMLParser import HTMLParser
from progressbar import *

class ISupError(Exception):
    pass

class NoFiles(ISupError):
    def __str__(self):
        return repr("Error: No Files to upload!")

class OptionError(ISupError):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
class ParseWorkaround(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.thmburl = attrs[0][1]
class ISup():
    """ Class for manage uploads
    Attributes:
        options  -- Options like resize
        FileList -- List of file names
        Request  -- Request list to be passed to PycURL
        Result   -- Upload details
    """
    def __init__(self, url, options = None):
        self.ISurl    = url
        self.options  = options
        self.cURLopts = []
        self.FileList = []
        self.Request  = []
        self.Return   = []
        self.Result   = {}

    def queue(self, Filename):
        self.FileList.append(Filename)

    def _makeRequest(self):
        if len(self.FileList) == 0:
            raise NoFiles()
        else:
            self.Request.append(("format", "json"))
            for o, a in [x for x in self.options]:
                if o == "RESIZE_IMAGE":
                    self.Request.append(('optimage', 1))
                    self.Request.append(('optsize', a))
                if o == "IMAGE_TAGS":
                    self.Request.append(('tags', a))
                elif o == "USER_USER":
                    self.Request.append(('a_username', a))
                elif o == "USER_PASSWORD":
                    self.Request.append(('a_password', a))
                elif o == "USER_COOKIE":
                    self.Request.append(('cookie', a))
                elif o == "API_KEY":
                    self.Request.append(('key', a))
                elif o == "CURL_VERBOSE":
                    self.cURLopts.append('verbose')
                elif o == "CURL_PROGRESSBAR":
                    self.cURLopts.append('progress')
                else:
                    raise OptionError("Unknown Option: {0:>s}".format(o))

    def _parseJSON(self, JSON):
        ## if error in JSON json class raise
        result = json.loads(JSON)

        self.Result['WIDTH']        = result["resolution"]["width"]
        self.Result['HEIGHT']       = result["resolution"]["height"]
        self.Result['UP_VIS']       = result["visibility"]
        self.Result['IP']           = result["uploader"]["ip"]
        self.Result['COOKIE']       = result["uploader"]["cookie"]
        self.Result['USER']         = result["uploader"]["username"]
        self.Result['URL']          = result["links"]["image_link"]
        self.Result['CODE_BB_THMB'] = result["links"]["thumb_bb2"]

        ## This is an workaround for this bug:
        ## http://code.google.com/p/imageshackapi/issues/detail?id=41
        self.Result['URL_THMB'], self.Result['CODE_H_THMB'] = \
                                self._workaround(result["links"]["thumb_link"])
    def _workaround(self, html):
        wa = ParseWorkaround()
        wa.feed(html)

        return wa.thmburl, html
    def _upload(self):
        cup = cURL(self.ISurl)
        if len(self.cURLopts) == 0:
            JSON = cup.getJSON(self.Request, progress = True, verbose = False)
        elif 'verbose' in self.cURLopts:
            JSON = cup.getJSON(self.Request, progress = False, verbose = True)
        elif 'progress' in self.cURLopts:
            JSON = cup.getJSON(self.Request, progress = True, verbose = False)
        ## CleanUp needed variables
        self.Request = []
        self.Result  = {}

        self._parseJSON(JSON)


    def upload(self):
        for f in self.FileList:
            if os.path.isfile(f):
                self._makeRequest()
                self.Request.append(("fileupload", (pycurl.FORM_FILE, f)))
                self._upload()
                self.Return.append(self.Result)
            else:
                raise IOError(2, "No such file or directory: {0:>s}".format(o))
        return self.Return


class cURL:
    """ cURL class used in ISup """
    def __init__(self, url):
        self.URL = url
        self.cp = pycurl.Curl()
        ## progressbar
        pyih_widget = ['UPLOAD: ', Percentage(), ' ', Bar(marker='#',
                                    left='[',right=']'), ' ', ETA(), ' ',
                                    FileTransferSpeed("k")]
        self.pb = ProgressBar(widgets = pyih_widget, maxval = 100)

    def _progress(self, dt, dd, ut, ud):
        current = (ud != 0) and int(ud / ut * 100) or 1
        if not current == self.pb.percentage():
            self.pb.update(current)


    def getJSON(self, POST, progress = True, verbose = False):
        self.cp.setopt(self.cp.POST, 1)
        self.cp.setopt(self.cp.HTTPPOST, POST)
        self.cp.setopt(self.cp.URL, self.URL)

        if progress:
            self.pb.start()
            self.cp.setopt(self.cp.NOPROGRESS, 0)
            self.cp.setopt(self.cp.PROGRESSFUNCTION, self._progress)
        if verbose:
            self.cp.setopt(self.cp.VERBOSE, 1)
            self.cp.setopt(self.cp.DEBUGFUNCTION, self._debug)

        result = StringIO()
        self.cp.setopt(self.cp.WRITEFUNCTION, result.write)
        self.cp.perform()

        if progress:
            self.pb.finish()

        return result.getvalue()

    def _debug(self, dtype, dmsg):
        sys.stdout.write("PycURL: ({0:d}): {1:>s}".format(dtype, dmsg))
