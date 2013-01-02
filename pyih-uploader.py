#!/usr/bin/env python2

# GPLv3

import sys, os, re, subprocess, gettext, pycurl
import xml.etree.ElementTree as ET
from utils import *

## Options
IMAGESHACK_URL = "http://www.imageshack.us/upload_api.php"
IMAGESHACK_KEY = "47DHIJMSe847793024d16f9db3e6f7b0d31389cc"
ONLY_PRINT_URL = False
ONLY_PRINT_THB = False
SEND_CLIPBOARD = False
RESIZE_IMAGE   = False
USER_USER      = False
USER_PASSWORD  = False
USER_COOKIE    = False
POST           = []

## Settings of gettext
if os.path.isdir(os.path.join(os.getcwd(), "locale")):
	gettext.bindtextdomain("pyih-uploader", os.path.join(os.getcwd(), "locale"))
else:
	gettext.bindtextdomain("pyih-uploader", None)
gettext.textdomain("pyih-uploader")
_ = gettext.gettext

VERSION = "PyIH-uploader version: 0.1.7"

def show_help(quit = True, code = 1):
	if quit == True:
		print _("HELPMSG")
		exit(code)
	else:
		print _("HELPMSG")

def create_request():
	global POST
	## Resize image ?
	if RESIZE_IMAGE != False:
		POST += [('optsize', 1), ('optsize', RESIZE_IMAGE)]

	## Save to account ?
	if USER_USER != False and USER_PASSWORD == False:
		print _("Missing Password")
		exit(1)
	elif USER_USER == False and USER_PASSWORD != False:
		print _("Missing Username")
		exit(1)
	elif USER_USER != False and USER_PASSWORD != False:
		POST += [('a_username', USER_USER), ('a_password', USER_PASSWORD)]

	## Save to account, using cookie ?
	if USER_COOKIE != False:
		POST += [('cookie', USER_COOKIE)]

	## Add image path to POST request
	if os.path.isfile(sys.argv[len(sys.argv) - 1]):
		POST += [('fileupload', (pycurl.FORM_FILE, sys.argv[len(sys.argv) - 1]))]
	else:
		print _("Open File Error")
		exit(1)

def parseXML(XML):
	UPLOAD = {}

	try:
		root = ET.fromstring(XML)
	except:
		print _("XML Parse Error")
		exit(2)

	## Resolution
	UPLOAD['width'] = root[2][0].text
	UPLOAD['height'] = root[2][1].text

	## Uploader
	UPLOAD['UP_IP'] = root[6][0].text
	UPLOAD['UP_CK'] = root[6][1].text
	UPLOAD['UP_US'] = root[6][2].text

	## Links
	UPLOAD['LNK_FULL'] = root[7][0].text
	UPLOAD['LNK_THMB'] = root[7][4].text

	return UPLOAD

def execute():
	global POST
	cup = cURL(IMAGESHACK_URL)

	POST += [('key', IMAGESHACK_KEY)]

	XML = cup.getXML(POST)
	#print XML
	#print POST

	## Parse XML and save details in UPLOAD
	UPLOAD = parseXML(XML)

	## Print upload details, or only URL
	if ONLY_PRINT_URL == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_FULL']
		if SEND_CLIPBOARD == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")
	elif ONLY_PRINT_THB == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_THMB']
		if SEND_CLIPBOARD == True:
			if copyToClipB(UPLOAD['LNK_THMB']) == False:
				print _("You need PyGTK to send to clipboard")
	else:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print _("UPLOAD_DETAILS: %1s %2s %3s %4s %5s %6s %7s") % \
									(UPLOAD['UP_IP'],
									UPLOAD['UP_US'],
									UPLOAD['UP_CK'],
									UPLOAD['width'],
									UPLOAD['height'],
									UPLOAD['LNK_FULL'],
									UPLOAD['LNK_THMB'])
		if SEND_CLIPBOARD == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")

def pass_args():
	global ONLY_PRINT_URL, ONLY_PRINT_THB, RESIZE_IMAGE
	global USER_USER, USER_PASSWORD, USER_COOKIE, SEND_CLIPBOARD
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-h" or sys.argv[i] == "--help":
			show_help(True, 0)
		elif sys.argv[i] == "-V" or sys.argv[i] == "--version":
			print VERSION
			exit(0)
		elif sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
			setopt('VERBOSE_OUTPUT', True)
		elif sys.argv[i] == "-u" or sys.argv[i] == "--url-only":
			ONLY_PRINT_URL = True
		elif sys.argv[i] == "-t" or sys.argv[i] == "--thb-only":
			ONLY_PRINT_THB = True
		elif sys.argv[i] == "-r" or sys.argv[i] == "--resize":
			RESIZE_IMAGE = sys.argv[i + 1]
		elif sys.argv[i] == "-K" or sys.argv[i] == "--clipboard":
			SEND_CLIPBOARD = True
		elif sys.argv[i] == "-U" or sys.argv[i] == "--user":
			USER_USER = sys.argv[i + 1]
		elif sys.argv[i] == "-P" or sys.argv[i] == "--pass":
			USER_PASSWORD = sys.argv[i + 1]
		elif sys.argv[i] == "-c" or sys.argv[i] == "--cookie":
			USER_COOKIE = sys.argv[i + 1]
		else:
			if os.path.isfile(sys.argv[len(sys.argv) - 1]) == False:
				print _("Error: Unknown Option: %1s") % sys.argv[i]
				show_help()

if len(sys.argv) <= 1 :
	show_help()
else:
	pass_args()
	DBG("Calling function: create_request()")
	create_request()
	DBG("Calling function: execute()")
	execute()
