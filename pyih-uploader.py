#!/usr/bin/env python2

# GPLv3

import sys, os, re, subprocess
import xml.etree.ElementTree as ET

VERSION = "PyIH-uploader version: 0.1"
HELPMSG = """
Usage: %s [options] filename
Options:
  -P|--pass pass  :       Your password (upload to your account, without cookie)
  -U|--user user  :       Your username (upload to your account, without cookie)
  -c|--cookie id  :       Use Registration code (upload to your account)
  -r|--resize WxH :       Resize image
  -u|--url-only   :       Only output the uploaded image url
  -V|--version    :       Show script version and exit
  -h|--help       :       Show this help message
"""

## Options
IMAGESHACK_KEY = "12678PUXfedd30dd950694fd9bc206662d4c6eb5"
ONLY_PRINT_URL = False
RESIZE_IMAGE   = False
USER_USER      = False
USER_PASSWORD  = False
USER_COOKIE    = False

COMMAND = "curl -s -F '"

def create_request():
	global COMMAND
	## Resize image ?
	if RESIZE_IMAGE != False:
		COMMAND += 'optsize=1&optsize=' + RESIZE_IMAGE

	## Save to account ?
	if USER_USER != False and USER_PASSWORD == False:
		print "You must specify password(-P|--pass)"
	elif USER_USER == False and USER_PASSWORD != False:
		print "You must specify username(-U|--user)"
	elif USER_USER != False and USER_PASSWORD != False:
		COMMAND += '&a_username=' + USER_USER + '&a_password=' + USER_PASSWORD

	## Save to account, using cookie ?
	if USER_COOKIE != False:
		COMMAND += 'cookie=' + USER_COOKIE

	## Add image path to COMMAND
	if os.path.isfile(sys.argv[len(sys.argv) - 1]):
		if COMMAND[-1] == "'":
			COMMAND += 'fileupload=@' + sys.argv[len(sys.argv) - 1]
		else:
			COMMAND += '&fileupload=@' + sys.argv[len(sys.argv) - 1]
	else:
		print "Sorry, error while opennig file to read, file exits ?"
		exit(1)

def parseXML(XML):
	UPLOAD = {}

	try:
		root = ET.fromstring(XML)
	except:
		print "Sorry, Error, try again!"
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

	COMMAND += ";type=image/" + ftype + "' " + 'http://www.imageshack.us/upload_api.php?key=' + IMAGESHACK_KEY

	print "Executing: " + COMMAND

	p = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, shell=True);
	XML = p.communicate()
	#print XML[0];

	## Parse XML and save details in UPLOAD
	UPLOAD = parseXML(XML[0])

	## Print upload details, or only URL
	if ONLY_PRINT_URL:
		print UPLOAD['LNK_FULL']
	else:
		print "Uploader:"
		print "  IP:", UPLOAD['UP_IP']
		print "  User:", UPLOAD['UP_US']
		print "  Cookie:", UPLOAD['UP_CK']
		print "Resolution:"
		print "  Width:", UPLOAD['width']
		print "  Height:", UPLOAD['height']
		print "Links:"
		print "  Original image:", UPLOAD['LNK_FULL']
		print "  Thumbnail image:", UPLOAD['LNK_THMB']

def pass_args():
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-h" or sys.argv[i] == "--help":
			print HELPMSG % sys.argv[0]
		elif sys.argv[i] == "-v" or sys.argv[i] == "--version":
			print VERSION
		elif sys.argv[i] == "-u" or sys.argv[i] == "--url-only":
			ONLY_PRINT_URL = True
		elif sys.argv[i] == "-r" or sys.argv[i] == "--resize":
			RESIZE_IMAGE = sys.argv[i + 1]
		elif sys.argv[i] == "-U" or sys.argv[i] == "--user":
			USER_USER = sys.argv[i + 1]
		elif sys.argv[i] == "-P" or sys.argv[i] == "--pass":
			USER_PASSWORD = sys.argv[i + 1]
		elif sys.argv[i] == "-c" or sys.argv[i] == "--cookie":
			USER_COOKIE = sys.argv[i + 1]

if len(sys.argv) <= 1 :
	print HELPMSG % sys.argv[0]
else:
	pass_args()
	create_request()
	execute()
