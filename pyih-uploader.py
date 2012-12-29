#!/usr/bin/env python2

# GPLv3

import sys, os, re, subprocess, gettext
import xml.etree.ElementTree as ET

## Options
IMAGESHACK_URL = "http://www.imageshack.us/upload_api.php"
IMAGESHACK_KEY = "12678PUXfedd30dd950694fd9bc206662d4c6eb5"
ONLY_PRINT_URL = False
ONLY_PRINT_THB = False
RESIZE_IMAGE   = False
USER_USER      = False
USER_PASSWORD  = False
USER_COOKIE    = False
COMMAND        = "curl -s"

## Settings of gettext
if os.path.isdir(os.path.join(os.getcwd(), "locale")):
	gettext.bindtextdomain("pyih-uploader", os.path.join(os.getcwd(), "locale"))
else:
	gettext.bindtextdomain("pyih-uploader", None)
gettext.textdomain("pyih-uploader")
_ = gettext.gettext

VERSION = "PyIH-uploader version: 0.1.5"

def create_request():
	global COMMAND
	## Resize image ?
	if RESIZE_IMAGE != False:
		COMMAND += ' -F "optsize=1&optsize=' + RESIZE_IMAGE + '"'

	## Save to account ?
	if USER_USER != False and USER_PASSWORD == False:
		print _("Missing Password")
		exit(1)
	elif USER_USER == False and USER_PASSWORD != False:
		print _("Missing Username")
		exit(1)
	elif USER_USER != False and USER_PASSWORD != False:
		COMMAND += ' -F "a_username=' + USER_USER + '&a_password=' + USER_PASSWORD + '"'

	## Save to account, using cookie ?
	if USER_COOKIE != False:
		COMMAND += ' -F "cookie=' + USER_COOKIE + '"'

	## Add image path to COMMAND
	if os.path.isfile(sys.argv[len(sys.argv) - 1]):
		COMMAND += ' -F "fileupload=@' + sys.argv[len(sys.argv) - 1]
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
	global COMMAND

	m = re.search('^.*\.([a-zA-Z]{3,4})$', sys.argv[len(sys.argv) - 1])

	ftype = m.group(1)
	if ftype == "jpg":
		ftype = "jpeg"

	COMMAND += ";type=image/" + ftype + '" ' + IMAGESHACK_URL + '?key=' + IMAGESHACK_KEY

	#print "Executing: " + COMMAND

	p = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, shell=True);
	XML = p.communicate()
	#print XML[0];

	## Parse XML and save details in UPLOAD
	UPLOAD = parseXML(XML[0])

	## Print upload details, or only URL
	if ONLY_PRINT_URL == True:
		print UPLOAD['LNK_FULL']
	elif ONLY_PRINT_THB == True:
		print UPLOAD['LNK_THMB']
	else:
		print _("UPLOAD_DETAILS: %1s %2s %3s %4s %5s %6s %7s") % \
									(UPLOAD['UP_IP'],
									UPLOAD['UP_US'],
									UPLOAD['UP_CK'],
									UPLOAD['width'],
									UPLOAD['height'],
									UPLOAD['LNK_FULL'],
									UPLOAD['LNK_THMB'])

def pass_args():
	global ONLY_PRINT_URL, ONLY_PRINT_THB, RESIZE_IMAGE, USER_USER, USER_PASSWORD, USER_COOKIE
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-h" or sys.argv[i] == "--help":
			print _("HELPMSG")
			exit(0)
		elif sys.argv[i] == "-v" or sys.argv[i] == "--version":
			print VERSION
			exit(0)
		elif sys.argv[i] == "-u" or sys.argv[i] == "--url-only":
			ONLY_PRINT_URL = True
		elif sys.argv[i] == "-t" or sys.argv[i] == "--thb-only":
			ONLY_PRINT_THB = True
		elif sys.argv[i] == "-r" or sys.argv[i] == "--resize":
			RESIZE_IMAGE = sys.argv[i + 1]
		elif sys.argv[i] == "-U" or sys.argv[i] == "--user":
			USER_USER = sys.argv[i + 1]
		elif sys.argv[i] == "-P" or sys.argv[i] == "--pass":
			USER_PASSWORD = sys.argv[i + 1]
		elif sys.argv[i] == "-c" or sys.argv[i] == "--cookie":
			USER_COOKIE = sys.argv[i + 1]

if len(sys.argv) <= 1 :
	print _("HELPMSG")
else:
	pass_args()
	create_request()
	execute()
