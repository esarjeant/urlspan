# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import locale
from locale import gettext as _
locale.textdomain('collage')

import logging
logger = logging.getLogger('collage')

from collage_lib.AboutDialog import AboutDialog

# See collage_lib.AboutDialog.py for more details about how this class works.
class AboutCollageDialog(AboutDialog):
    __gtype_name__ = "AboutCollageDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutCollageDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

