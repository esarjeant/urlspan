# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.urlspan.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from urlspan_lib.UrlSpanSettings import UrlSpanSettings

import locale
from locale import gettext as _
locale.textdomain('urlspan')

import logging
logger = logging.getLogger('urlspan')

from urlspan_lib.PreferencesDialog import PreferencesDialog

class PreferencesUrlSpanDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesUrlSpanDialog"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesUrlSpanDialog, self).finish_initializing(builder)

        # Code for other intialization actions should be added here.
        self.cc = UrlSpanSettings()

        cmbUserAgent = self.builder.get_object("cmbUserAgent")       
        self.setComboBoxByValue(cmbUserAgent, self.cc.getUserAgent())

        cmbAccept = self.builder.get_object("cmbAccept")
        self.setComboBoxByValue(cmbAccept, self.cc.getAccept())

    def setComboBoxByValue(self, cmb, val):

        # default to something sensible
        cmb.set_active(0)

        # try to match on the method val
        model = cmb.get_model()
        iterTree = model.get_iter_first()

        for i, k in enumerate(model):
            itr = model.get_iter(i)
            title = model.get_value(itr, 0)

            if title == val:
                cmb.set_active(i)
                break

        
    def on_btnCancel_clicked(self, widget):
        self.destroy()

    def on_btnOk_clicked(self, widget):
        cmbUserAgent = self.builder.get_object("cmbUserAgent")
       
        if cmbUserAgent.get_active_text() != None:
            agent = cmbUserAgent.get_active_text()
            self.cc.setUserAgent(agent)

        cmbAccept = self.builder.get_object("cmbAccept")
       
        if cmbAccept.get_active_text() != None:
            accept = cmbAccept.get_active_text()
            self.cc.setAccept(accept)

        self.cc.save()
        self.destroy()

