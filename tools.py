#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    @author Tomasz Kozubal
    @license GNU GPL v3
"""
import hashlib


def md5(str):
    import hashlib
    return hashlib.md5(str).hexdigest()

def md5file(file_path):
    try:
        with open(file_path) as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned
    except IOError:
        print("File not found: %s" % file_path)


def path2url(base_url=None, folder_path=None):
    import urlparse, urllib
    if base_url and folder_path:
        return urlparse.urljoin(
          base_url, urllib.pathname2url(folder_path))


def url2path(url):
    import urllib
    return urllib.url2pathname(url=url)
