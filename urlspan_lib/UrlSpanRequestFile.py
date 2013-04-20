# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# Store and retrieve UrlSpan request files. These are HTTP
# request/response with raw headers and such.

import os

class UrlSpanRequestFile:

    def __init__(self):
        self.requestUrl = "http://localhost"
        self.requestMethod = "GET"
        self.requestDocument = ""
        self.fileName = None
        self.contentType = "text/html"
        self.headers = {}
        pass

    def loadFile(self, file_name):
        self.fileName = file_name

        # track when payload processing (document) begins
        isDocBlock = False

        if os.path.exists(file_name):
            file = open(file_name)

            for line in file:

                if not isDocBlock:
                    self.parseHeader(line)
                else:
                    self.parseDocument(line)

                # determine if we will be in a docblock
                if not isDocBlock and line == '\n':
                    isDocBlock = True
                          

    def parseHeader(self, line):
        hdNameValue = line.split("\t", line.count("\t"))

        if (len(hdNameValue) > 1):

          pn = hdNameValue[0].strip(' ').strip('\n')
          pv = hdNameValue[1].strip(' ').strip('\n')

          if pn == "X-Request-URL":
              self.requestUrl = pv

          elif pn == "X-Request-Method":
              self.requestMethod = pv

          elif pn == "X-Content-Type":
              self.contentType = pv

          else:
              self.headers[pn] = pv

    def parseDocument(self, line):
        if self.requestDocument == None:
            self.requestDocument = line
        else:
            self.requestDocument += line

    def getFileName(self):
        return self.fileName

    def getRequestUrl(self):
        return self.requestUrl

    def setRequestUrl(self, url):
        self.requestUrl = url

    def getRequestMethod(self):
        return self.requestMethod
 
    def setRequestMethod(self, methodName):
        self.requestMethod = methodName

    def getRequestDocument(self):
        return self.requestDocument

    def setRequestDocument(self, doc):
        self.requestDocument = doc

    def getHeaderValue(self, key):
        pass

    def setHeaderValue(self, key, value):
        pass

    def setContentType(self, ct):
        self.contentType = ct

    def getContentType(self):
        return self.contentType

    def setFile(self, fn):
        if None == self.fileName:
            self.fileName = fn

    def save(self):
        print "Saving..."

        with open(self.fileName, 'wb', 0) as cf:
            cf.write("X-Request-URL\t%s\n" %(self.requestUrl))
            cf.write("X-Request-Method\t%s\n" %(self.requestMethod))
            cf.write("X-Content-Type\t%s\n" %(self.contentType))
            cf.write("\n")
            cf.write(self.requestDocument)

            cf.close()
        #with open(os.path.expanduser('~/.urlspan'), 'w') as configfile:
        #    config.write(configfile)




