#!/usr/bin/env python2
import sys, getopt, os, gettext
from config import O
from isup import ISup

## 
#* This file is part of PyIS-Upload, licensed
#* under GNU GPL at version 3 or any other version.
##


## Constants
IMAGESHACK_URL   = "https://post.imageshack.us/upload_api.php"
VERSION          = "PyIS-uploader version: 0.2"

# Install gettext
if os.path.isdir(os.path.join(os.getcwd(), "locale")):
    gettext.install("pyis-uploader", os.path.join(os.getcwd(), "locale"), unicode=1)
else:
    gettext.install("pyis-uploader", unicode=1)
# End gettext

# config
o = O()
# End config

class PyIH:
    def __init__(self):
        self.o = O()
        self.isopts = []

    def _isup(self, options):
        self.isup = ISup(IMAGESHACK_URL, options)

    def _isopts(self):
        if self.o.getopt('RESIZE_IMAGE'):
            self.isopts.append(('RESIZE_IMAGE', self.o.getopt('RESIZE_IMAGE')))
        elif self.o.getopt('USER_USER') and self.o.getopt('USER_PASSWORD'):
            self.isopts.append(('USER_USER', self.o.getopt('USER_USER')))
            self.isopts.append(('USER_PASSWORD', self.o.getopt('USER_PASSWORD')))
        elif self.o.getopt('USER_COOKIE'):
            self.isopts.append(('USER_COOKIE', self.o.getopt('USER_COOKIE')))
        elif self.o.getopt('VERBOSE_OUTPUT'):
            self.isopts.append(('CURL_VERBOSE', True))
        elif self.o.getopt('ONLY_PRINT_URL') or self.o.getopt('ONLY_PRINT_THB'):
            self.isopts.append(('CURL_PROGRESSBAR', True))

        self.isopts.append(('API_KEY', o.getopt('IMAGESHACK_KEY')))

    def _show_help(self, quit = True, code = 1):
        if quit == True:
            print _("HELPMSG")
            exit(code)
        else:
            print _("HELPMSG")

    def pass_args(self):
        if len(sys.argv) <= 1:
            self._show_help()

        try:
            sopt = "P:U:c:r:KtufvVh"
            lopt = "pass= user= cookie= resize= clipboard thb-only url-only full-details verbose version help".split()
            opts, args = getopt.getopt(sys.argv[1:], sopt, lopt)
        except getopt.GetoptError as err:
            print str(err)
            sys.exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                self._show_help(True, 0)
            elif o in ("-V", "--version"):
                print VERSION
                exit(0)
            elif o in ("-v", "--verbose"):
                self.o.setopt('VERBOSE_OUTPUT', True)
            elif o in ("-u", "--url-only"):
                self.o.setopt('ONLY_PRINT_URL', True)
            elif o in ("-t", "--thb-only"):
                self.o.setopt('ONLY_PRINT_THB', True)
            elif o in ("-f", "--full-details"):
                self.o.setopt('PRINT_FULL_IN_M', True)
            elif o in ("-r", "--resize"):
                self.o.setopt('RESIZE_IMAGE', a)
            elif o in ("-K", "--clipboard"):
                self.o.setopt('SEND_CLIPBOARD', True)
            elif o in ("-U", "--user"):
                self.o.setopt('USER_USER', a)
            elif o in ("-P", "--pass"):
                self.o.setopt('USER_PASSWORD', a)
            elif o in ("-c", "--cookie"):
                self.o.setpt('USER_COOKIE', a)

        self._isopts()
        self._isup(self.isopts)
        for a in args:
            if not os.path.isfile(a):
                print _("Error: File not found: %1s  Ignoring...") % a
            else:
                self.isup.queue(a)

    def send(self):
        self.details = self.isup.upload()
        if len(self.details) == 1:
            if self.o.getopt("ONLY_PRINT_URL"):
                print self._printURL(self.details[0])
            elif self.o.getopt("ONLY_PRINT_THB"):
                print self._printTHMB(self.details[0])
            else:
                self._printfull(self.details[0])
        else:
            if self.o.getopt("PRINT_FULL_IN_M"):
                for d in self.details:
                    self._printfull(d)
            elif self.o.getopt("ONLY_PRINT_THB"):
                for d in self.details:
                    self._printTHMB(d)
            else:
                for d in self.details:
                    self._printURL(d)



    def _printfull(self, details):
        print _("UPLOAD_DETAILS: %1s %2s %3s %4s %5s %6s %7s") % (details['UP_IP'], details['UP_US'], details['UP_CK'], details['width'], details['height'], details['LNK_FULL'], details['LNK_THMB'])
    def _printURL(self, details):
        print details['LNK_FULL']
    def _printTHMB(self, details):
        print details['LNK_THMB']

if __name__ == "__main__":
    pyih = PyIH()
    pyih.pass_args()
    pyih.send()
