from gtk import *
from gtk.gdk import Pixbuf, pixbuf_new_from_file_at_size


class PreferencesDialog(Dialog):
    def __init__(self):
        super(PreferencesDialog, self).__init__("Preferences - PyIS-Uploader")
        
        self._box = self.get_content_area()
        ## Notebook
        self._nb = Notebook()
        
        ## Notebook pages
        self._general = Frame()
        self._account = Frame()
        self._account_()
        
        self._nb.append_page(self._general, Label("General"))
        self._nb.append_page(self._account, Label("Account"))
        self._box.pack_start(self._nb)
        
        self._sets()
    def _sets(self):
        self.add_button(STOCK_APPLY, RESPONSE_APPLY)
        self.add_button(STOCK_CANCEL, RESPONSE_CANCEL)
        self.add_button(STOCK_OK, RESPONSE_OK)
        
        self._nb.set_tab_pos(POS_TOP)
    
    def _general(self):
        pass
    def _account_(self):
        vbox = VBox()
        huser = HBox()
        hpass = HBox()
        
        luser = Label("Username:")
        lpass = Label("Password:")
        tuser = Entry()
        tpass = Entry()
        
        huser.pack_start(luser)
        huser.pack_end(tuser)
        hpass.pack_start(lpass)
        hpass.pack_end(tpass)
        vbox.pack_start(huser)
        vbox.pack_end(hpass)
        
        self._account.add(vbox)
    def show(self):
        self.show_all()
        return self.run()

class MainWindow():
    def __init__(self):
        self._mw = Window()
        self._vbox = VBox()
        self._agr = AccelGroup()
        self._mw.add_accel_group(self._agr)
        ## Menu's
        self._mbar = MenuBar()
        File = [
                (ImageMenuItem(STOCK_ADD, self._agr), self._cb_open, "<Control>O"),
                (ImageMenuItem(STOCK_REMOVE, self._agr), self._cb_remove, "<Control>R"),
                (SeparatorMenuItem(), None, None),
                (ImageMenuItem(STOCK_PREFERENCES, self._agr), self._cb_open_prefs, "<Control>P"),
                (SeparatorMenuItem(), None, None),
                (ImageMenuItem(STOCK_QUIT, self._agr), self._cb_exit, "<Control>Q")
                ]
        Queue = [
                (ImageMenuItem(STOCK_GOTO_TOP, self._agr), self._cb_goto_top, "<Shift>T"),
                (ImageMenuItem(STOCK_GOTO_BOTTOM, self._agr), self._cb_goto_bottom, "<Shift>B"),
                (SeparatorMenuItem(), None, None),
                (ImageMenuItem(STOCK_GO_BACK, self._agr), self._cb_go_back, "<Shift>Up"),
                (ImageMenuItem(STOCK_GO_FORWARD, self._agr), self._cb_go_forward, "<Shift>Down")
        ]
        Help = [
                (ImageMenuItem(STOCK_ABOUT, self._agr), self._cb_about, None)
        ]
        self._Menus = [
                (MenuItem("_File"), File),
                (MenuItem("_Queue"), Queue),
                (MenuItem("_Help"), Help)
                ]
        self._menus()
        ## Toolbar
        self._tb = Toolbar()
        self._TBItens = [
                (ToolButton(STOCK_ADD), self._cb_open),
                (ToolButton(STOCK_REMOVE), self._cb_remove),
                (SeparatorToolItem(), None),
                (ToolButton(STOCK_GOTO_TOP), self._cb_goto_top),
                (ToolButton(STOCK_GO_BACK), self._cb_go_back),
                (ToolButton(STOCK_GO_FORWARD), self._cb_go_forward),
                (ToolButton(STOCK_GOTO_BOTTOM), self._cb_goto_bottom),
                (SeparatorToolItem(), None),
                (ToolButton(STOCK_APPLY), self._cb_apply)
        ]
        self._toolbar()
        ## Statusbar
        self._sb = HBox()
        self._SBItens = [
                (ProgressBar(), None)
        ]
        self._sbar()
        ## Queue (IconView)
        self._sw = ScrolledWindow()
        self._sw.set_shadow_type(SHADOW_ETCHED_IN)
        self._sw.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
        
        self._ls = ListStore(Pixbuf, str)
        self._iv = IconView(self._ls)
        
        self._filelist = list()
    def _menus(self):
        for m in self._Menus:
            m[0].set_submenu(self._submenu(m[1]))
            self._mbar.append(m[0])
            
    def _submenu(self, sm):
        menu = Menu()
        for si in sm:
            if si[2] == None:
                if not si[1] == None:
                    si[0].connect("activate", si[1])
                    menu.append(si[0])
                else:
                    menu.append(si[0])
            else:
                if not si[1] == None:
                    key, mod = accelerator_parse(si[2])
                    si[0].add_accelerator("activate", self._agr, key, mod, ACCEL_VISIBLE)
                    si[0].connect("activate", si[1])
                    menu.append(si[0])
        return menu
    def _toolbar(self):
        for t in self._TBItens:
            if t[1] == None:
                self._tb.insert(t[0], -1)
            else:
                self._tb.insert(t[0], -1)
                t[0].connect("clicked", t[1])
    def _sbar(self):
        for i in self._SBItens:
           self._sb.pack_start(i[0], expand=True)
    def _sets(self):
        self._mw.set_size_request(628, 500)
        self._mw.set_title("PyIS-Uploader - GUI (GTK+)")
        
        for t in self._TBItens:
            t[0].set_expand(True)
            
        self._iv.set_pixbuf_column(0)
        self._iv.set_text_column(1)
    def _show(self):
        self._sets()
        self._mw.add(self._vbox)
        
        self._sw.add(self._iv)
        
        self._vbox.pack_start(self._mbar, expand=False, fill=False)
        self._vbox.pack_start(self._tb, expand=False, fill=False)
        self._vbox.pack_start(self._sw, expand=True, fill=True)
        self._vbox.pack_end(self._sb, expand=False, fill=False)
        
        self._mw.show_all()
    def _connect(self):
        self._mw.connect("delete_event", self._cb_exit)
    def show(self):
        self._connect()
        self._show()
        main()
    ## Callback's
    def _cb_exit(self, widget, event=None):
        if event == None:
            self._mw.destroy()
        print "Okay... Exiting..."
        main_quit()
    def _cb_open_prefs(self, button):
        prefs = PreferencesDialog()
        print prefs.show()
        prefs.destroy()
    def _cb_open(self, button):
        dlg_open = FileChooserDialog("Open Image", button.get_toplevel(), FILE_CHOOSER_ACTION_OPEN,
                                    (STOCK_CANCEL, RESPONSE_CANCEL, STOCK_OPEN, RESPONSE_OK))
        dlg_open.set_default_response(1)
        dlg_open.set_select_multiple(True)
        
        filef = FileFilter()
        filef.add_pixbuf_formats()
        dlg_open.set_filter(filef)
        
        if dlg_open.run() == RESPONSE_OK:
            for f in dlg_open.get_filenames():
                img = pixbuf_new_from_file_at_size(f, 128, 128)
                
                name = f.split('/')[-1]
                if len(name) > 18:
                    name = name[:8] + '...' + name[-8:]
                
                self._ls.append([img, name])
                
                self._filelist.append(f)
        dlg_open.destroy()
            
    def _cb_remove(self, button):
        model = self._iv.get_model()
        c = self._iv.get_cursor()
        if not c == None:
            it = model.get_iter(c[0])
            self._ls.remove(it)
    def _cb_goto_top(self, button):
        model = self._iv.get_model()
        c = self._iv.get_cursor()
        if not c == None:
            it = model.get_iter(c[0])
            self._ls.move_after(it, None)
            
            self._filelist.insert(0, self._filelist.pop(c[0][0]))
    def _cb_goto_bottom(self, button):
        model = self._iv.get_model()
        c = self._iv.get_cursor()
        if not c == None:
            it = model.get_iter(c[0])
            self._ls.move_before(it, None)
            
            self._filelist.append(self._filelist.pop(c[0][0]))
    def _cb_go_back(self, button):
        model = self._iv.get_model()
        c = self._iv.get_cursor()
        if not c == None and not c[0][0] == 0:
            path = (c[0][0] - 1,)
            pos = model.get_iter(path)
            it = model.get_iter(c[0])
            self._ls.move_before(it, pos)
            
            self._filelist.insert(path[0], self._filelist.pop(c[0][0]))
    def _cb_go_forward(self, button):
        model = self._iv.get_model()
        c = self._iv.get_cursor()
        if not c == None and not c[0][0] == len(model) - 1:
            path = (c[0][0] + 1,)
            pos = model.get_iter(path)
            it = model.get_iter(c[0])
            self._ls.move_after(it, pos)
            
            self._filelist.insert(path[0], self._filelist.pop(c[0][0]))
    def _cb_apply(self, button):
        print self._filelist
    def _cb_about(self, button):
        pass