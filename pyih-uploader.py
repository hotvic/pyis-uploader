#!/usr/bin/env python2

# GPLv3

import sys, os, re, subprocess, gettext, pycurl
import xml.etree.ElementTree as ET
from utils import *

## Constants
IMAGESHACK_URL   = "http://www.imageshack.us/upload_api.php"
VERSION          = "PyIH-uploader version: 0.1.7"
## Global variables
POST           = []

## Settings of gettext
if os.path.isdir(os.path.join(os.getcwd(), "locale")):
	gettext.bindtextdomain("pyih-uploader", os.path.join(os.getcwd(), "locale"))
else:
	gettext.bindtextdomain("pyih-uploader", None)
gettext.textdomain("pyih-uploader")
_ = gettext.gettext

def show_help(quit = True, code = 1):
	if quit == True:
		print _("HELPMSG")
		exit(code)
	else:
		print _("HELPMSG")

def create_request():
	global POST
	## Resize image ?
	if getopt('RESIZE_IMAGE') != False:
		POST += [('optsize', 1), ('optsize', getopt('RESIZE_IMAGE'))]

	## Save to account ?
	if getopt('USER_USER') != False and getopt('USER_PASSWORD') == False:
		print _("Missing Password")
		exit(1)
	elif getopt('USER_USER') == False and getopt('USER_PASSWORD') != False:
		print _("Missing Username")
		exit(1)
	elif getopt('USER_USER') != False and getopt('USER_PASSWORD') != False:
		POST += [('a_username', getopt('USER_USER')), ('a_password', getopt('USER_PASSWORD'))]

	## Save to account, using cookie ?
	if getopt('USER_COOKIE') != False:
		POST += [('cookie', getopt('USER_COOKIE'))]

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

	POST += [('key', getopt('IMAGESHACK_KEY'))]

	XML = cup.getXML(POST)
	#print XML
	#print POST

	## Parse XML and save details in UPLOAD
	UPLOAD = parseXML(XML)

	## Print upload details, or only URL
	if getopt('ONLY_PRINT_URL') == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_FULL']
		if getopt('SEND_CLIPBOARD') == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")
	elif getopt('ONLY_PRINT_THB') == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_THMB']
		if getopt('SEND_CLIPBOARD') == True:
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
		if UPLOAD['UP_US'] == "PyIHUploader":
			print _("(Warning: Your upload saved on account of PyIHUploader)")
		if getopt('SEND_CLIPBOARD') == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")

def pass_args():
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-h" or sys.argv[i] == "--help":
			show_help(True, 0)
		elif sys.argv[i] == "-V" or sys.argv[i] == "--version":
			print VERSION
			exit(0)
		elif sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
			setopt('VERBOSE_OUTPUT', True)
		elif sys.argv[i] == "-u" or sys.argv[i] == "--url-only":
			setopt('ONLY_PRINT_URL', True)
		elif sys.argv[i] == "-t" or sys.argv[i] == "--thb-only":
			setopt('ONLY_PRINT_THB', True)
		elif sys.argv[i] == "-r" or sys.argv[i] == "--resize":
			setopt('RESIZE_IMAGE', sys.argv[i + 1])
		elif sys.argv[i] == "-K" or sys.argv[i] == "--clipboard":
			setopt('SEND_CLIPBOARD', True)
		elif sys.argv[i] == "-U" or sys.argv[i] == "--user":
			setopt('USER_USER', sys.argv[i + 1])
		elif sys.argv[i] == "-P" or sys.argv[i] == "--pass":
			setopt('USER_PASSWORD', sys.argv[i + 1])
		elif sys.argv[i] == "-c" or sys.argv[i] == "--cookie":
			setpt('USER_COOKIE', sys.argv[i + 1])
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
