#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    @author Tomasz Kozubal
    @license GNU GPL v3
"""

import os

class Conf:
    def __init__(self, instance=None):
        self.prog_dir = '/home/tomakoz/dev/'
        self.db_dir = os.path.join(self.prog_dir, 'db')
        self.download_dir = '/media/tomakoz/DATA/'
