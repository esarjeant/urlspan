# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import httplib2
import locale
import gobject
import urllib
from locale import gettext as _
locale.textdomain('collage')

from gi.repository import Gtk, Gdk # pylint: disable=E0611
import logging
logger = logging.getLogger('collage')

from collage_lib import Window
from collage.AboutCollageDialog import AboutCollageDialog
from collage.PreferencesCollageDialog import PreferencesCollageDialog

from collage_lib.CollageSettings import CollageSettings
from collage_lib.CollageRequestFile import CollageRequestFile

#from lxml.html.soupparser import fromstring
#from lxml.etree import tostring

# See collage_lib.Window.py for more details about how this class works
class CollageWindow(Window):
    __gtype_name__ = "CollageWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(CollageWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutCollageDialog
        self.PreferencesDialog = PreferencesCollageDialog

        self.config = CollageSettings()

        # Code for other initialization actions should be added here.
        self.cmbHttpMethod = self.builder.get_object("cmbHttpMethod")
        self.cmbContentType = self.builder.get_object("cmbContentType")
        self.txtUrl = self.builder.get_object("txtUrl")
        self.txtRequest = self.builder.get_object("txtRequest")
        self.txtResponse = self.builder.get_object("txtResponse")
        self.lblStatus = self.builder.get_object("lblStatus") 

        self.open_dialog = None
        self.FileOpenDialog = self.builder.get_object("FileOpenDialog")       

        # read from config file....        
        self.cfgFile = None
        self.resetForm()
 
    def on_btnRequest_clicked(self, widget):

        method = self.getHttpMethod()
        contentType = self.getHttpContentType()
        body = self.getRequestDocument()

        headers = {'Content-type': contentType, 'Accept': self.config.getAccept()}
        url = self.getHttpRequestUrl()

        # request the raw response
        resp, content = httplib2.Http().request(url, method, headers=headers, body=body)
        txtResponseBuf = self.txtResponse.get_buffer()
        txtResponseBuf.set_text(content)

        # handle the error somehow...
        self.lblStatus.set_text(
"Status: %s; Content-Length: %s; Content-Type: %s" % (resp['status'], resp['content-length'], resp['content-type']))

    def resetForm(self):
        self.setHttpMethod("")
        self.txtUrl.set_text("")
        self.setHttpContentType("")

        txtRequestBuf = self.txtRequest.get_buffer()
        txtRequestBuf.set_text("")

        txtResponseBuf = self.txtResponse.get_buffer()
        txtResponseBuf.set_text("")

    def getRequestDocument(self):
        txtRequestBuf = self.txtRequest.get_buffer()
        body = txtRequestBuf.get_text(txtRequestBuf.get_start_iter(), txtRequestBuf.get_end_iter(), False)

        return body

    def getHttpMethod(self):

        method = "GET"
        if self.cmbHttpMethod.get_active_text() != None:
            method = self.cmbHttpMethod.get_active_text()

        return method

    def getHttpRequestUrl(self):
        return self.txtUrl.get_text()

    def getHttpContentType(self):
        contentType = "text/plain"
        if self.cmbContentType.get_active_text() != None:
            contentType = self.cmbContentType.get_active_text()

        return contentType


    def on_btnDecode_clicked(self, widget):  
        txtResponseBuf = self.txtResponse.get_buffer()

        raw = txtResponseBuf.get_text(txtResponseBuf.get_start_iter(), txtResponseBuf.get_end_iter(), False)

        rawunenc = urllib.unquote(raw)
        #rawdoc = fromstring(rawunenc)
        #sgmlstr = tostring(rawdoc, pretty_print=True).strip()

        txtResponseBuf.set_text(rawunenc)


    def setHttpMethod(self, methodVal):

        # default to something sensible
        self.cmbHttpMethod.set_active(0)

        # try to match on the method val
        model = self.cmbHttpMethod.get_model()
        iterTree = model.get_iter_first()

        for i, k in enumerate(model):
            itr = model.get_iter(i)
            title = model.get_value(itr, 0)

            if title == methodVal:
                self.cmbHttpMethod.set_active(i)
                break

    def setHttpContentType(self, typeVal):

        print "invoking setHttpContentType with [%s]" % (typeVal)

        # default to something sensible
        self.cmbContentType.set_active(0)

        # try to match on the method val
        model = self.cmbContentType.get_model()
        iterTree = model.get_iter_first()

        for i, k in enumerate(model):
            itr = model.get_iter(i)
            title = model.get_value(itr, 0)

            if title == typeVal:
                self.cmbContentType.set_active(i)
                break

    def on_mnu_new_activate(self, widget, data=None):
        if self.cfgFile != None:
            # TODO: prompt warning file needs to be saved
            self.cfgFile = None

        # reset the rest of the form
        self.resetForm()
        

    def on_mnu_save_activate(self, widget, data=None):

        dialog = Gtk.FileChooserDialog("Save As", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL,  
                                        Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if self.cfgFile == None:
            response = dialog.run()

            # open the specified file
            if response == Gtk.ResponseType.OK:
                self.cfgFile = CollageRequestFile()
                self.cfgFile.setFile(dialog.get_filename())
        

        if self.cfgFile != None:
            self.cfgFile.setRequestMethod(self.getHttpMethod())
            self.cfgFile.setRequestUrl(self.getHttpRequestUrl())
            self.cfgFile.setContentType(self.getHttpContentType())
            self.cfgFile.setRequestDocument(self.getRequestDocument())

            self.cfgFile.save()

        # remove dialog
        dialog.destroy()

    def on_mnu_open_activate(self, widget, data=None):
        dialog = Gtk.FileChooserDialog("Open File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL,  
                                       Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
           
            # open the specified file
            self.cfgFile = CollageRequestFile()
            self.cfgFile.loadFile(dialog.get_filename())

            # use these settings
            self.setHttpMethod(self.cfgFile.getRequestMethod())
            self.txtUrl.set_text(self.cfgFile.getRequestUrl())
            self.setHttpContentType(self.cfgFile.getContentType())

            txtRequestBuf = self.txtRequest.get_buffer()
            txtRequestBuf.set_text(self.cfgFile.getRequestDocument())

        dialog.destroy()

    def on_mnu_paste_enc_activate(self, widget, data=None):
        clippy = Gtk.Clipboard().get(Gdk.SELECTION_CLIPBOARD)
        doc = clippy.wait_for_text()

        if doc != None:
           docenc = urllib.quote(doc)

           txtRequestBuf = self.txtRequest.get_buffer()
           txtRequestBuf.insert_at_cursor(docenc)


