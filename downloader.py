#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    @author Tomasz Kozubal
    @license GNU GPL v3
"""
import ssl
import urllib2
import BeautifulSoup
import os
import sys
import cPickle as pickle

class Downloader:
    def __init__(self, base_url=None, url=None, dl_dir=None):
        if not base_url:
            base_url = 'https://b2b.knode.online:8080/public/projekty/'
        if not dl_dir:
            dl_dir = '/home/tomakoz/bajzel/public/projekty/'
        self.dl_dir = dl_dir
        self.base_url = base_url
        self.current_url = url
        self.db_dir = os.path.join(os.getcwd(), 'db')
        self.current_db_dir = os.path.join(self.db_dir, 'b2b.knode.online')
        self.data = None
        self.urls = dict()
        self.dirsHistory = list()
        self.filesHistory = list()
        self.dirsIndex = dict()
        self.filesIndex = list()
        self.hashes = list()
        self.filesIndexPath = os.path.join(self.current_db_dir, 'scanner_fIndex.p')
        self.dirsIndexPath = os.path.join(self.current_db_dir, 'scanner_dIndex.p')
        self.filesHistoryPath = os.path.join(self.current_db_dir, 'scanner_fHistory.p')
        self.dirsHistoryPath = os.path.join(self.current_db_dir, 'scanner_dHistory.p')
        self.storage_path = '/media/tomakoz/DATA/public/projekty/'
        self.init_db()
        if not base_url:
            base_url = 'https://b2b.knode.online:8080/public/projekty/'
        self.base_url = base_url
        if not url:
            url = self.base_url
        self.current_url = url
        self.code = 0
        self.data = None
        if url:
            self.fetch_content()
        self.init_db()

    def init_db(self):
        if not os.path.isdir(self.current_db_dir):
            os.makedirs(self.current_db_dir)
        if not os.path.isdir(self.dl_dir):
            os.makedirs(self.dl_dir)
        self.get_db()

    def get_db(self):
        if os.path.isfile(self.dirsIndexPath):
            # self.dirsIndex = pickle.load(open(self.dirsIndexPath, "rb"))
            self.filesIndex = pickle.load(open(self.filesIndexPath, "rb"))
            # self.dirsHistory = pickle.load(open(self.dirsHistoryPath, "rb"))
            self.filesHistory = pickle.load(open(self.filesHistoryPath, "rb"))

    def save_index(self):
        # pickle.dump(self.dirsIndex, open(self.dirsIndexPath, "wb"))
        pickle.dump(self.filesIndex, open(self.filesIndexPath, "wb"))
        # pickle.dump(self.dirsHistory, open(self.dirsHistoryPath, "wb"))
        pickle.dump(self.filesHistory, open(self.filesHistoryPath, "wb"))

    def fetch_content(self, url=None):
        if url:
            self.current_url = url
        context = ssl._create_unverified_context()
        request = urllib2.urlopen(self.current_url, context=context)
        self.code = request.code
        self.data = request.read()

    # def save_content(self):
    def dl(self, url=None):
        if not url:
            url = self.current_url
        uri_param = self.current_url.split('/')
        if '?' in uri_param[0]:
            request_uri = uri_param[0].split('?')
            file_name=request_uri[0]
        else:
            file_name = uri_param

        file_path = url
        file_dir = url.replace(self.base_url, self.dl_dir)
        print("file_dir: %s" % file_dir)
        print("file_name: %s" % file_name)
        # self.fetch_content(self.current_url)

        # with open(file_name, 'wa') as f:
        # f.write(self.data)
        # with fs in self.data:
        #     open(self.)


def main():
    dl = Downloader()
    for hash in dl.filesIndex:
        print(hash)
        dl.dl(hash)
        sys.exit(1)
    print(dl.data)

if __name__ == '__main__':
    main()