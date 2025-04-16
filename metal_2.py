#!/usr/bin/python

import urllib2
import os

class Metal:

    def __init__(self):
        self.base_url = 'https://b2b.knode.online:8080/public/projekty/'
        self.current_url = ''
        self.data = ''

    def get_index(self, url=None):
        if not url:
            self.current_url = self.base_url
        else:
            self.current_url = url

        request = urllib2.open(self.current_url)
        self.data = request.read()
        print(self.data)