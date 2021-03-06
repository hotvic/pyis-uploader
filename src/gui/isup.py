import os, sys, pycurl, json
from StringIO import StringIO
from HTMLParser import HTMLParser

## 
#* This file is part of PyIS-Upload, licensed
#* under GNU GPL at version 3 or any other version.
##

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

        self.Result['width']    = result["resolution"]["width"]
        self.Result['height']   = result["resolution"]["height"]
        self.Result['UP_VIS']   = result["visibility"]
        self.Result['UP_IP']    = result["uploader"]["ip"]
        self.Result['UP_CK']    = result["uploader"]["cookie"]
        self.Result['UP_US']    = result["uploader"]["username"]
        self.Result['LNK_FULL'] = result["links"]["image_link"]

        ## This is an workaround for this bug: http://code.google.com/p/imageshackapi/issues/detail?id=41
        self.Result['LNK_THMB'], self.Result['CODE_H_THB'] = self._wordaround(result["links"]["thumb_link"])
    def _wordaround(self, html):
        wa = ParseWorkaround()
        wa.feed(html)

        return wa.thmburl, html
    def _upload(self, progresshandler):
        cup = cURL(self.ISurl, progresshandler)
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


    def upload(self, progresshandler=None):
        for f in self.FileList:
            if os.path.isfile(f):
                self._makeRequest()
                self.Request.append(("fileupload", (pycurl.FORM_FILE, f)))
                self._upload(progresshandler)
                self.Return.append(self.Result)
            else:
                raise IOError(2, "No such file or directory: {0:>s}".format(o))
        return self.Return


class cURL:
    """ cURL class used in ISup """
    def __init__(self, url, progresshandler=None):
        self.URL = url
        self.cp = pycurl.Curl()
        ## progressbar
        if not progresshandler:
            from progressbar import Percentage, Bar, ETA, FileTransferSpeed, ProgressBar
            
            pyis_widget = ['UPLOAD: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'), ' ', ETA(), ' ', FileTransferSpeed("K")]
            self.pb = ProgressBar(widgets = pyis_widget, maxval = 100)
            self.progresshandler = self._progress
        else:
            self.progresshandler = progresshandler

    def _progress(self, dt, dd, ut, ud):
        current = (ud != 0) and int(ud / ut * 100) or 1
        if not current == self.pb.percentage():
            self.pb.update(current)


    def getJSON(self, POST, progress = True, verbose = False):
        self.cp.setopt(self.cp.POST, 1)
        self.cp.setopt(self.cp.HTTPPOST, POST)
        self.cp.setopt(self.cp.URL, self.URL)

        if progress and self.progresshandler == self._progress:
            self.pb.start()
            self.cp.setopt(self.cp.NOPROGRESS, 0)
            self.cp.setopt(self.cp.PROGRESSFUNCTION, self.progresshandler)
        elif progress and not self.progresshandler == self._progress:
            self.cp.setopt(self.cp.NOPROGRESS, 0)
            self.cp.setopt(self.cp.PROGRESSFUNCTION, self.progresshandler)
        if verbose:
            self.cp.setopt(self.cp.VERBOSE, 1)
            self.cp.setopt(self.cp.DEBUGFUNCTION, self._debug)

        result = StringIO()
        self.cp.setopt(self.cp.WRITEFUNCTION, result.write)
        self.cp.perform()

        if progress and self.progresshandler == self._progress:
            self.pb.finish()

        return result.getvalue()

    def _debug(self, dtype, dmsg):
        sys.stdout.write("PycURL: ({0:d}): {1:>s}".format(dtype, dmsg))
