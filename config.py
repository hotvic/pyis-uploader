## 
#* This file is part of PyIS-Upload, licensed
#* under GNU GPL at version 3 or any other version.
##

class O:
	def __init__(self):
		self.opts = {
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
	def getopt(self, optname):
		return self.opts[optname]
	def getopts(self):
		return self.opts
	def setopt(self, optname, value = None):
		self.opts[optname] = value
	def save(self):
		pass
