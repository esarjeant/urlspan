# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.collage.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from collage_lib.CollageSettings import CollageSettings

import locale
from locale import gettext as _
locale.textdomain('collage')

import logging
logger = logging.getLogger('collage')

from collage_lib.PreferencesDialog import PreferencesDialog

class PreferencesCollageDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesCollageDialog"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesCollageDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        #settings = Gio.Settings("net.launchpad.collage")
        #widget = self.builder.get_object('example_entry')
        #settings.bind("example", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        # Code for other intialization actions should be added here.
        self.cc = CollageSettings()
        
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
