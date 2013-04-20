# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import locale
from locale import gettext as _
locale.textdomain('urlspan')

import logging
logger = logging.getLogger('urlspan')

from urlspan_lib.AboutDialog import AboutDialog

# See urlspan_lib.AboutDialog.py for more details about how this class works.
class AboutUrlSpanDialog(AboutDialog):
    __gtype_name__ = "AboutUrlSpanDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutUrlSpanDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

