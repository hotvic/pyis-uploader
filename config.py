import os, ConfigParser

ACC_DEFAULT = {
        "username": "blabla",
        "sumpass": "sumpass"
}
class Config(ConfigParser.ConfigParser):
    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)
        
        self._configfile = self.openconfig()
        if not self._configfile[1]:
            self.write_default()
    def openconfig(self):
        configdir = os.getenv('HOME') + '/.pyis-uploader'
        configfile = configdir + '/gui.ini'
        
        if not os.path.isdir(configdir):
            os.mkdir(configdir)

        if not os.path.isfile(configfile):
            try:
                self._f = open(configfile, 'wb')
                return self._f, False
            except OSError as e:
                print e
                return None, False
        else:
            try:
                self._f = open(configfile, 'wb')
                return self._f, True if os.path.getsize(configfile) > 0 else False
            except OSError as e:
                print e
                return None, True
    def write_default(self):
        self.add_section('ACCOUNT')
        for c in ACC_DEFAULT:
            self.set('ACCOUNT', c, ACC_DEFAULT[c])
        self.write(self._f)