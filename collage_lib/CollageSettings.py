# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This can store/retrieve application preferences.

import ConfigParser, os

class CollageSettings:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.expanduser('~/.collage'))

        if config.has_option("Preferences", "user_agent"):
            self.userAgent = config.get("Preferences", "user_agent")
        else:
            self.userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20110506 Firefox/4.0.1"

        if config.has_option("Preferences", "http_accept"):
            self.httpAccept = config.get("Preferences", "http_accept")
        else:
            self.httpAccept = "*/*"

    def getUserAgent(self):
        return self.userAgent

    def setUserAgent(self, agent):
        self.userAgent = agent

    def getAccept(self):
        return self.httpAccept

    def setAccept(self, accept):
        self.httpAccept = accept

    def save(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.expanduser('~/.collage'))

        if (not config.has_section("Preferences")):
            config.add_section("Preferences")

        config.set("Preferences", "user_agent", self.userAgent)
        config.set("Preferences", "http_accept", self.httpAccept)

        with open(os.path.expanduser('~/.collage'), 'wb') as configfile:
            config.write(configfile)
