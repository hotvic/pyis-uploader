#!/usr/bin/env python2

# GPLv3

import sys, getopt, os, re, subprocess, gettext, pycurl
import xml.etree.ElementTree as ET
from utils import *

## Constants
IMAGESHACK_URL   = "http://www.imageshack.us/upload_api.php"
VERSION          = "PyIH-uploader version: 0.1.9"
## Global variables
POST             = []

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
	if ogetopt('RESIZE_IMAGE') != False:
		POST += [('optsize', 1), ('optsize', ogetopt('RESIZE_IMAGE'))]

	## Save to account ?
	if ogetopt('USER_USER') != False and ogetopt('USER_PASSWORD') == False:
		print _("Missing Password")
		exit(1)
	elif ogetopt('USER_USER') == False and ogetopt('USER_PASSWORD') != False:
		print _("Missing Username")
		exit(1)
	elif ogetopt('USER_USER') != False and ogetopt('USER_PASSWORD') != False:
		POST += [('a_username', ogetopt('USER_USER')), ('a_password', ogetopt('USER_PASSWORD'))]

	## Save to account, using cookie ?
	if ogetopt('USER_COOKIE') != False:
		POST += [('cookie', ogetopt('USER_COOKIE'))]

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

	POST += [('key', ogetopt('IMAGESHACK_KEY'))]

	XML = cup.getXML(POST)
	#print XML
	#print POST

	## Parse XML and save details in UPLOAD
	UPLOAD = parseXML(XML)

	## Print upload details, or only URL
	if ogetopt('ONLY_PRINT_URL') == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_FULL']
		if ogetopt('SEND_CLIPBOARD') == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")
	elif ogetopt('ONLY_PRINT_THB') == True:
		sys.stdout.write("\r")
		sys.stdout.flush()
		print UPLOAD['LNK_THMB']
		if ogetopt('SEND_CLIPBOARD') == True:
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
		if ogetopt('SEND_CLIPBOARD') == True:
			if copyToClipB(UPLOAD['LNK_FULL']) == False:
				print _("You need PyGTK to send to clipboard")

def pass_args():
	try:
		sopt = "P:U:c:r:KtuvVh"
		lopt = "pass= user= cookie= resize= clipboard thb-only url-only verbose version help".split()
		opts, args = getopt.getopt(sys.argv[1:], sopt, lopt)
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(1)
	for o, a in opts:
		if o in ("-h", "--help"):
			show_help(True, 0)
		elif o in ("-V", "--version"):
			print VERSION
			exit(0)
		elif o in ("-v", "--verbose"):
			osetopt('VERBOSE_OUTPUT', True)
		elif o in ("-u", "--url-only"):
			osetopt('ONLY_PRINT_URL', True)
		elif o in ("-t", "--thb-only"):
			osetopt('ONLY_PRINT_THB', True)
		elif o in ("-r", "--resize"):
			osetopt('RESIZE_IMAGE', a)
		elif o in ("-K", "--clipboard"):
			osetopt('SEND_CLIPBOARD', True)
		elif o in ("-U", "--user"):
			osetopt('USER_USER', a)
		elif o in ("-P", "--pass"):
			osetopt('USER_PASSWORD', a)
		elif o in ("-c", "--cookie"):
			osetpt('USER_COOKIE', a)
	for a in args:
		if not os.path.isfile(a):
			print _("Error: File not found: %1s") % a
			exit(1)
		else:
			return
	print _("Error: Please specify file name")
	exit(1)

if len(sys.argv) <= 1 :
	show_help()
else:
	pass_args()
	DBG("Calling function: create_request()")
	create_request()
	DBG("Calling function: execute()")
	execute()
