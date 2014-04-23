# -*- coding: UTF-8 -*-

from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from threading import Thread
from common import get_ui_path

# from .isup import ISup

LICENSE = """
Copyright © 2013,2014 Victor A. Santos <victoraur.santos@gmail.com>

PyIS-Uploader is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyIS-Uploader is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# class PreferencesDialog(Dialog):
#     def __init__(self):
#         super(PreferencesDialog, self).__init__("Preferences - PyIS-Uploader")
        
#         self._box = self.get_content_area()
#         ## Notebook
#         self._nb = Notebook()
        
#         ## Notebook pages
#         self._general = Frame()
#         self._account = Frame()
#         self._account_()
        
#         self._nb.append_page(self._general, Label("General"))
#         self._nb.append_page(self._account, Label("Account"))
#         self._box.pack_start(self._nb)
        
#         self._sets()
#     def _sets(self):
#         self.add_button(STOCK_APPLY, RESPONSE_APPLY)
#         self.add_button(STOCK_CANCEL, RESPONSE_CANCEL)
#         self.add_button(STOCK_OK, RESPONSE_OK)
        
#         self._nb.set_tab_pos(POS_TOP)
    
#     def _general(self):
#         pass
#     def _account_(self):
#         vbox = VBox()
#         huser = HBox()
#         hpass = HBox()
        
#         luser = Label("Username:")
#         lpass = Label("Password:")
#         self._tuser = Entry()
#         self._tpass = Entry()
        
#         huser.pack_start(luser)
#         huser.pack_end(self._tuser)
#         hpass.pack_start(lpass)
#         hpass.pack_end(self._tpass)
#         vbox.pack_start(huser)
#         vbox.pack_end(hpass)
        
#         self._account.add(vbox)
#     def show(self):
#         self.show_all()
#         return self.run()
#     def get_acc_user(self):
#         return self._tuser.get_text()
#     def set_acc_user(self, value):
#         self._tuser.set_text(value)


class PyISGUI(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="org.hotvic.pyis-uploader-gui-gtk3")

        # Builder
        self.builder = Gtk.Builder.new_from_file(get_ui_path('mainwindow.ui'))

        # Main Window
        self._mw = self.builder.get_object('mw')

        # The queue ListStore
        self.queue_ls = self.builder.get_object('queue_ls')

        # handlers
        handlers = {
            # File Menu Callbacks
            "onAddImg": self._cb_open,
            "onRemoveImg": self._cb_remove,
            "onOpenPrefs": self._cb_open_prefs,
            "onQuit": self._cb_exit,
            # Queue Menu callbacks
            "onGoToTop": self._cb_goto_top,
            "onGoToBottom": self._cb_goto_bottom,
            "onGoBack": self._cb_go_back,
            "onGoForward": self._cb_go_forward,
            # Help Menu Callbacks
            "onAbout": self._cb_about
        }
        self.builder.connect_signals(handlers)

        # connect app signals and register
        self.connect('startup', self.startup)
        self.register()

    def startup(self, app):
        self.add_window(self._mw)

    def show(self):
        self._mw.show_all()
        Gtk.main()

    ## Callbacks
    def _cb_exit(self, widget, event=None):
        if event == None:
            self._mw.destroy()
        Gtk.main_quit()
        self.release()

    def _cb_open_prefs(self, button):
        #prefs = PreferencesDialog()
        #print prefs.show()
        #prefs.destroy()
        nimsg = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK, message_format="Sorry, Not Implemented yet!")
        nimsg.run()
        nimsg.destroy()

    def _cb_open(self, button):
        dlg_open = Gtk.FileChooserDialog(
                                         "Open Image",
                                         button.get_toplevel(),
                                         Gtk.FileChooserAction.OPEN,
                                         (
                                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
                                         ))
        dlg_open.set_default_response(1)
        dlg_open.set_select_multiple(True)
        
        filef = Gtk.FileFilter()
        filef.add_pixbuf_formats()
        dlg_open.set_filter(filef)
        
        if dlg_open.run() == Gtk.ResponseType.OK:
            for f in dlg_open.get_filenames():
                img = Pixbuf.new_from_file_at_size(f, 128, 128)
                
                name = f.split('/')[-1]
                if len(name) > 18:
                    name = name[:8] + '...' + name[-8:]
                
                self.queue_ls.append([img, name, f])
        dlg_open.destroy()
            
    def _cb_remove(self, button):
        cursor, path, cell = self.builder.get_object('queue_iv').get_cursor()
        if cursor:
            self.queue_ls.remove(ls.get_iter(path))

    def _cb_goto_top(self, button):
        cursor, path, cell = self.builder.get_object('queue_iv').get_cursor()
        if cursor:
            self.queue_ls.move_after(ls.get_iter(path), None)

    def _cb_goto_bottom(self, button):
        cursor, path, cell = self.builder.get_object('queue_iv').get_cursor()
        if cursor:
            self.queue_ls.move_before(ls.get_iter(path), None)

    def _cb_go_back(self, button):
        cursor, path, cell = self.builder.get_object('queue_iv').get_cursor()
        if cursor and not path.get_indices()[0] == 0:
            it = self.queue_ls.get_iter(path)
            path.prev()
            pos = self.queue_ls.get_iter(path)
            
            self.queue_ls.move_before(it, pos)

    def _cb_go_forward(self, button):
        cursor, path, cell = self.builder.get_object('queue_iv').get_cursor()
        if cursor and not path.get_indices()[0] == len(self.queue_ls) - 1:
            it = self.queue_ls.get_iter(path)
            path.next()
            pos = self.queue_ls.get_iter(path)
            
            self.queue_ls.move_after(it, pos)

    def _cb_apply(self, button):
        options = [('API_KEY' ,'47DHIJMSe847793024d16f9db3e6f7b0d31389cc')]#, ('CURL_VERBOSE', True)]
        isup = ISup("https://post.imageshack.us/upload_api.php", options)
        
        while len(self._filelist) != 0:
            self._SBItens[0][0].set_text(self._filelist[0])
            
            isup.queue(self._filelist[0])
            
            Result = isup.upload(self._on_progress)
            self._on_upload_finish(Result[0])
            
            ## Remove uploaded itens
            self._filelist.pop(0)
            model = self._iv.get_model()
            it = model.get_iter((0,))
            self._ls.remove(it)

    def _on_upload_finish(self, details):
        rdlg = Dialog("Uploaded", buttons=(STOCK_CLOSE, RESPONSE_CLOSE))
        vbox = rdlg.get_content_area()
        hbup = HBox()
        hbwi = HBox()
        hbhg = HBox()
        hblf = HBox()
        hblt = HBox()
        hbch = HBox()
        hbcb = HBox()
        
        vbox.pack_start(hbup)
        vbox.pack_start(hbwi)
        vbox.pack_start(hbhg)
        vbox.pack_start(hblf)
        vbox.pack_start(hblt)
        vbox.pack_start(hbch)
        vbox.pack_start(hbcb)
        
        ## Uploader
        ul_user = Label("Uploader:")
        ue_user = Entry()
        ue_user.set_property('editable', False)
        ue_user.set_text(details['UP_US'])
        hbup.pack_start(ul_user)
        hbup.pack_start(ue_user)
        
        ## Image
        il_width = Label("Width:")
        ie_width = Entry()
        ie_width.set_property('editable', False)
        ie_width.set_text(str(details['width']))
        il_height = Label("Height:")
        ie_height = Entry()
        ie_height.set_property('editable', False)
        ie_height.set_text(str(details['height']))
        hbwi.pack_start(il_width)
        hbwi.pack_start(ie_width)
        hbhg.pack_start(il_height)
        hbhg.pack_start(ie_height)
        
        ## links, and code
        ll_url = Label("Full Image Link:")
        le_url = Entry()
        le_url.set_property('editable', False)
        le_url.set_text(details['LNK_FULL'])
        ll_thb = Label("Thumbnail Link:")
        le_thb = Entry()
        le_thb.set_property('editable', False)
        le_thb.set_text(details['LNK_THMB'])
        cl_html = Label("HTML Code:")
        ce_html = Entry()
        ce_html.set_property('editable', False)
        ce_html.set_text("Sorry, Not Implemented!")
        cl_bbc = Label("BB Code:")
        ce_bbc = Entry()
        ce_bbc.set_property('editable', False)
        ce_bbc.set_text("Sorry, Not Implemented!")
        hblf.pack_start(ll_url)
        hblf.pack_start(le_url)
        hblt.pack_start(ll_thb)
        hblt.pack_start(le_thb)
        hbch.pack_start(cl_html)
        hbch.pack_start(ce_html)
        hbcb.pack_start(cl_bbc)
        hbcb.pack_start(ce_bbc)
        
        rdlg.show_all()
        rdlg.run()
        rdlg.destroy()

    def _on_progress(self, dt, dd, ut, ud):
        current = (ud != 0) and int(ud / ut * 100) or 1
        current /= 100
        
        if not current == self._SBItens[0][0].get_fraction():
            self._SBItens[0][0].set_fraction(current)
            while events_pending():
                main_iteration()

    def _cb_about(self, button):
        about = Gtk.AboutDialog()
        
        about.set_program_name("PyIS-Uploader GUI")
        about.set_version("0.2a Beta")
        about.set_copyright("Copyright © 2014 - Victor A. Santos")
        about.set_comments("PyIS-Uploader GUI(Graphical User Interface) for PyIS-Uploader, Written in Python and GTK.\n\nPyIS-Uploader is a powerful tool written in python that uses PycURL to send image files to ImageShack, a great site for image file share.")
        about.set_license(LICENSE)
        about.set_website("https://github.com/hotvic/pyis-uploader/")
        about.set_website_label("Home Page on GitHub")
        about.set_authors("Victor A. Santos <victoraur.santos@gmail.com>")
        
        about.run()
        about.destroy()