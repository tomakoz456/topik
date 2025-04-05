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
import cPickle as pickle
from downloader import Downloader
from tools import md5
from conf import Conf as conf

class Scanner:
    def __init__(self, base_url=None, url=None):
        self.c = conf()
        # self.ignore_extension = list('lnk', 'Thumbs.db')
        if not base_url:
            base_url = 'https://b2b.knode.online:8080/public/projekty/'
        self.base_url = base_url
        self.current_url = url
        self.db_dir = self.c.db_dir
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
        self.init_db()
        self.dl = Downloader()

    def log(self, msg):
        print("%s" % msg)

    def init_db(self):
        if not os.path.isdir(self.current_db_dir):
            os.makedirs(self.current_db_dir)
        self.get_db()

    def fetch_url(self, url=None):
        if url:
            self.current_url = url
        self.log("start fetch content: %s" % url)
        self.dl.fetch_content(self.current_url)
        self.log("end fetch content: %s" % url)
        if self.dl.code is 200:
            self.data = self.dl.data
            path = self.current_url.replace(self.base_url, '')
            hash = md5(path)
            if hash in self.hashes:
                del(self.hashes[hash])
            if self.current_url in self.dirsIndex:
                self.dirsHistory.append(self.current_url)
                del(self.dirsIndex[self.current_url])
            if self.current_url in self.filesIndex:
                self.filesHistory.append(self.current_url)
                del(self.filesIndex[self.current_url])
        else:
            print("error HTTP CODE")

    def get_db(self):
        if os.path.isfile(self.dirsIndexPath):
            self.dirsIndex = pickle.load(open(self.dirsIndexPath, "rb"))
            self.filesIndex = pickle.load(open(self.filesIndexPath, "rb"))
            self.dirsHistory = pickle.load(open(self.dirsHistoryPath, "rb"))
            self.filesHistory = pickle.load(open(self.filesHistoryPath, "rb"))

    def save_index(self):
        pickle.dump(self.dirsIndex, open(self.dirsIndexPath, "wb"))
        pickle.dump(self.filesIndex, open(self.filesIndexPath, "wb"))
        pickle.dump(self.dirsHistory, open(self.dirsHistoryPath, "wb"))
        pickle.dump(self.filesHistory, open(self.filesHistoryPath, "wb"))


    def add_url(self, anchor):
        if "%s" % anchor['href'][0] != '?':
            if anchor['href'][-1] == '/':
                if anchor.text != 'Parent Directory':
                    hash = md5(anchor['href'])
                    print("hash: %s, url: %s" % (hash, anchor['href']))
                    if hash not in self.dirsIndex.keys():
                        self.dirsIndex[hash] = "%s%s" % (self.current_url, anchor['href'])
                        self.hashes.append(hash)


            else:
                # self.setToDownload("%s%s" % (self.current_url, anchor['href']))
                self.filesIndex.append("%s%s" % (self.current_url,
                                            anchor['href']))

    def add_to_scanner(self, url):
        pass

    def add_to_download(self, url):
        pass

    # def setToDownload(self, url):


    def parse_html(self, data=None):
        if data:
            self.data = data
        soup = BeautifulSoup.BeautifulSoup(self.data)
        for anchor in soup.findAll('a', href=True):
            self.add_url(anchor)


def main():
    scanner = Scanner()
    scanner.get_db()
    scanner.fetch_url(scanner.base_url)
    scanner.parse_html()
    print(scanner.dirsIndex)
    print(scanner.filesIndex)
    print(len(scanner.dirsIndex))
    # while dir in scanner.dirsIndex:
    i = 0
    for hash in scanner.hashes:
        scanner.fetch_url(scanner.dirsIndex[hash])
        scanner.parse_html()
        # i += 1
        # if i == 2:
        #     break
    # for dirs in scanner.dirsIndex:
    #     scanner.fetch_url(scanner.dirsIndex[dirs])
    #     scanner.parse_html()
    scanner.save_index()

if __name__ == '__main__':
    main()