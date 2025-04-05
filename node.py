#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    @author Tomasz Kozubal
    @license GNU GPL v3
"""

import sys
import os
import tools


class Node:
    def __init__(self, base_path):
        self.base_path = base_path
        self.hash = None
        self.full_path = None
        self.path = None
        self.