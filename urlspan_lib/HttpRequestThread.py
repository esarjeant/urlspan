# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# Threaded implementation of HTTP request/respons with callback.

import gobject
import time
import threading
import httplib2

from threading import Thread

from urlspan_lib.UrlSpanSettings import UrlSpanSettings


class HttpRequestThread(threading.Thread):

    def __init__(self, condition, url):
        #super(HttpRequestThread, self).__init__()
        #self.setDaemon(False)
        self.condition = condition        
        Thread.__init__(self)

        self.url = url
        self.method = "GET"
        self.contentType = "text/none"
        self.body = ""
        self.accept = "*/*"

        self.respContent = ""
        self.respStatus = "0"
        self.respContentLength = 0
        self.respContentType = "*/*"

        self.error = None

    def setMethod(self, name):
        self.method = name

    def setContentType(self, ct):
        self.contentType = ct
 
    def setBody(self, data):
        self.body = data

    def setAccept(self, acc):
        self.accept = acc

    def run(self):

        try:

            config = UrlSpanSettings()

            bodyLength = len(self.body)
            print ("content-length: %s" % str(bodyLength))

            headers = {'user-agent': config.getUserAgent(), 'content-type': self.contentType, 'accept': self.accept}

            # request the raw response
            print "sending request to httplib2..."
            resp, content = httplib2.Http().request(self.url, self.method, headers=headers, body=self.body)
            print "received response from httplib2..."
        
            # parse the response
            self.respContent = content
            self.respStatus = resp['status']
            self.respContentLength = len(self.respContent)
            self.respContentType = resp['content-type']

        except Exception, e:
            print "Error in run()"
            self.error = e.message

        finally:
            with self.condition:
                self.condition.notify()

    def getResponseContent(self):
        return self.respContent

    def getResponseMessage(self):
        return ("Status: %s; Content-Length: %s; Content-Type: %s" % (self.respStatus, self.respContentLength, self.respContentType))
 
    def getError(self):
         return self.error

    def hasError(self):
         return (self.error != None)
