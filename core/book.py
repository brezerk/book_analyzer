#!env python
# -*- coding: utf-8 -*-

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import csv
import sys
import string
import random

from itertools import groupby
from operator import itemgetter

# app imports
from core.defines import *
from core.logger import logger
from core.exceptions import FileLoadError

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"


class BookAnalyzer:
    """
    Implements BookAnalyzer core logic

    Properties:
    """

    def __init__(self, target_size):
        """
        Initialize the board and map
        Generate an board with random chars if x and y passed
        """
        self.__target_size = target_size
        self.__stream = sys.stdin

    def load(cls, target_size, filename):
        """
        Load board from csv file returns an class instance

        Keyword arguments:
            filename -- full path to the file
        """
        if not os.path.exists(filename):
            raise FileLoadError("File '%s' not found" % filename)

        instance = cls(target_size=target_size)
        instance.__stream = open(filename, 'r')

        return instance

    def run(self):
        print("Logic")
