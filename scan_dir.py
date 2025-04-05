#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    @author Tomasz Kozubal
    @license GNU GPL v3
"""
# /media/tomakoz/DATA/

import sys
import os
import tools
import cPickle as pickle
from  conf import Conf as conf

class ScanDir:
    def __init__(self, dir_path=None, index_path=None):
        self.c = conf()
        self.index = None
        if not dir_path:
            dir_path = '/media/tomakoz/DATA/public/projekty/'
        self.base_url = 'https://b2b.knode.online:8080/public/projekty/'
        self.base_dir = dir_path
        self.dirsIndex = dict()
        self.filesIndex = dict()
        self.files_index_file = 'tkDirIndex.p'
        self.dirs_index_file = 'tkFileIndex.p'
        self.index_file = 'tkFilenamesIndex.p'
        self.db_dir = self.c.db_dir
        self.current_db_dir = os.path.join(self.db_dir, 'b2b.knode.online')
        if not index_path:
            index_path = os.path.join(self.base_dir, self.index_file)
        self.index_path = index_path


    def load_index(self, index_path=None):
        if not index_path:
            self.index_path = index_path
        try:
            self.index = pickle.load(open(os.path.join(self.current_db_dir, self.index_path), 'rb'))
        except IOError:
            self.index = dict()
        try:
            self.dirsIndex = pickle.load(open(os.path.join(self.current_db_dir, self.dirs_index_file), 'rb'))
        except IOError:
            self.dirsIndex = dict()
        try:
            self.filesIndex = pickle.load(open(os.path.join(self.current_db_dir, self.files_index_file), 'rb'))
        except IOError:
            self.filesIndex = dict()

    def save_index(self, index_path=None):
        if not index_path:
            self.index_path = index_path
        index_path = os.path.join(self.current_db_dir, self.index_file)
        pickle.dump(self.index, open(os.path.join(self.current_db_dir, self.index_file), "wb"))
        if os.path.isfile(index_path):
            print("Index path: %s" % index_path)
        else:
            print("error Index path not found in %s" % index_path)
        pickle.dump(self.dirsIndex, open(os.path.join(self.current_db_dir, self.dirs_index_file), 'wb'))
        pickle.dump(self.filesIndex, open(os.path.join(self.current_db_dir, self.files_index_file), 'wb'))

    def scan(self, dir_path=None):
        import urllib
        # try:
        base_dir = r'/home/tomakoz/dev/'
        tmp_file = 'files.p'
        tmp_dirs = 'dirs.p'
        tmp_file_path = os.path.join(base_dir, tmp_file)
        tmp_dirs_path = os.path.join(base_dir, tmp_dirs)
        # dir_list = dict()
        # file_list = dict()
        x = 0
        print(tmp_dirs_path)
        if not dir_path:
            self.base_dir = dir_path
        for root, sub_folder, files in os.walk(self.base_dir):
            print(root)
            print(sub_folder)
            print(files)
            # sys.exit(1)
            dir_index = open(tmp_dirs_path, 'wa')
            if len(sub_folder) > 0:
                for folder in sub_folder:
                    folder_full_path = os.path.join(root, folder)

                    if os.path.isdir(folder_full_path):
                        print("folder_full_path: %s" % folder_full_path)
                    folder_path = folder_full_path.replace(self.base_dir, '')
                    folder_path_uri = tools.path2url(base_url=self.base_url, folder_path=folder_path)
                    folder_uri = urllib.pathname2url(folder_path)
                    folder_hash = tools.md5(folder_path_uri)
                    if folder_hash not in self.dirsIndex.keys():
                        self.dirsIndex[folder_hash] = {'path': folder_path, 'uri':folder_uri}
                        print("add: %s: %s" % (folder_hash, folder_path))

            if len(files) > 0:
                for file in files:
                    file_full_path = os.path.join(root, file)
                    if os.path.isfile(file_full_path):
                        print("file_full_path: %s" % file_full_path)
                    else:
                        print("file not exist: %s" % file_full_path)
                    file_path = file_full_path.replace(self.base_url, '')
                    file_path_uri = tools.path2url(base_url=self.base_url, folder_path=file_path)
                    file_uri = urllib.pathname2url(file_path)
                    file_hash = tools.md5(file_path_uri)
                    if file_hash not in self.filesIndex.keys():
                        self.filesIndex[file_hash] = {'path': file_path, 'uri': file_uri}
                        print("add: %s: %s" % (file_hash, file_path))
                x += 1
                if x == 3:
                    self.save_index()
                    sys.exit(1)
        # except Exception as e:
        #     print("Error scan: %r" % e)



def main():
    sc = ScanDir()
    try:
        sc.scan(r'/media/tomakoz/DATA/public/projekty')
        sc.save_index()
    except KeyboardInterrupt:
        sc.save_index()
        print("Close program")
        sys.exit()

if __name__ == '__main__':
    main()
