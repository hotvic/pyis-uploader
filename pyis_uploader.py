#!/usr/bin/env python2
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

import sys, os, argparse, gettext
import config
from isup import ISup

## Constants
IMAGESHACK_URL = "https://post.imageshack.us/upload_api.php"
VERSION        = 'PyIS-Uploader 0.2'

# Install gettext
gettext.install("pyis-uploader", unicode=1)

## Messages
UP_DETAILS = _("""\
Uploader:
  IP: %(IP)s
  User: %(USER)s
  Cookie: %(COOKIE)s
Resolution:
  Width: %(WIDTH)s
  Height: %(HEIGHT)s
Links:
  Original image: %(URL)s
  Thumbnail image: %(URL_THMB)s
Codes:
  Thumbnail:
    HTML: %(CODE_H_THMB)s
    BBCode: %(CODE_BB_THMB)s""")

class PyIS:
    def __init__(self):
        self.o = config.Config()
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
        elif self.o.getopt('IMAGE_TAGS'):
            self.isopts.append(('IMAGE_TAGS', self.o.getopt('IMAGE_TAGS')))
        elif self.o.getopt('VERBOSE_OUTPUT'):
            self.isopts.append(('CURL_VERBOSE', True))
        elif self.o.getopt('ONLY_PRINT_URL') or self.o.getopt('ONLY_PRINT_THB'):
            self.isopts.append(('CURL_PROGRESSBAR', True))

        self.isopts.append(('API_KEY', self.o.getopt('IMAGESHACK_KEY')))

    def pass_args(self):
        parser = argparse.ArgumentParser(prog='pyis-uploader', usage='%(prog)s [options] IMG [IMG ...]',
                                         description='PyIS-Uploader (Python ImageShack Uploader) is small python2 program to upload images to ImageShack')
        # Add arguments
        parser.add_argument('img', metavar='IMG', nargs='+', help='Image files to upload')
        parser.add_argument('--pwd', '-P', help='Your password (upload to your account, without cookie)')
        parser.add_argument('--user', '-U', help='Your username (upload to your account, without cookie)')
        parser.add_argument('--cookie', '-c', help='Use Registration code (upload to your account)')
        parser.add_argument('--resize', '-r', help='Resize image')
        parser.add_argument('--tags', '-T', help='Add tags to uploaded image(CSV format)')
        parser.add_argument('--clipboard', '-K', action='store_true', help='Send uploaded image url to clipboard(GTK)')
        parser.add_argument('--thb-only', '-t', action='store_true', help='Only output the uploaded image url (Thumbnail)')
        parser.add_argument('--url-only', '-u', action='store_true', help='Only output the uploaded image url')
        parser.add_argument('--full-details', '-f', action='store_true', help='When uploading multiple images this option make print all details of all images')
        parser.add_argument('--verbose', '-v', action='store_true', help='Show debug messages')
        parser.add_argument('--version', '-V', action='version', version=VERSION)

        args = parser.parse_args()

        self.o.setopt('VERBOSE_OUTPUT', args.verbose)
        self.o.setopt('ONLY_PRINT_URL', args.url_only)
        self.o.setopt('ONLY_PRINT_THB', args.thb_only)
        self.o.setopt('PRINT_FULL_IN_M', args.full_details)
        self.o.setopt('SEND_CLIPBOARD', args.clipboard)
        if args.resize:
            self.o.setopt('RESIZE_IMAGE', a)
        elif args.tags:
            self.o.setopt('IMAGE_TAGS', a)
        elif args.user:
            self.o.setopt('USER_USER', a)
        elif args.pwd:
            self.o.setopt('USER_PASSWORD', a)
        elif args.cookie:
            self.o.setpt('USER_COOKIE', a)

        self._isopts()
        self._isup(self.isopts)
        for img in args.img:
            if not os.path.isfile(img):
                print _("Error: File not found: %(name)s  Ignoring...") % {'name': img}
            else:
                self.isup.queue(img)

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
        self.o.close()

    def _printfull(self, details):
        print UP_DETAILS % details

    def _printURL(self, details):
        print details['URL']

    def _printTHMB(self, details):
        print details['URL_THMB']

if __name__ == "__main__":
    pyis = PyIS()
    pyis.pass_args()
    pyis.send()
