#!env python
# -*- coding: utf-8 -*-

"""
Test assigment:

Your task is to write a program, BookAnalyzer, that analyzes such a log file.
BookAnalyzer takes one command line argument: target‐size. BookAnalyzer then
reads a market data log on standard input. As the book is modified,
BookAnalyzer prints (on standard output) the total expense you would incur if
you bought target‐size shares (by taking as many asks as necessary, lowest
first), and the total income you would receive if you sold target‐size shares
(by hitting as many bids as necessary, highest first). Each time the income or
expense changes, it prints the changed value.

"""

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
import sys
import errno

# we need >= 3.4 b/c of queue, threading module naming changes
# yeah, if it is needed we can support 2.x and 3.x branches, but hey
# this is kinda out of the scope, right? :D
try:
    assert sys.version_info >= (3, 4)
except AssertionError:
    print("ERROR: Python >= 3.4 is REQUIRED")
    sys.exit(errno.ENOPKG)

import re
import argparse
import logging

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

# app imports
from core.logger import logger, handler
from core.defines import *
from core.book import BookAnalyzer
from core.exceptions import ValidationError
from core.utils import die

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Analyzes incoming market
        data log stream and prints out the total expense you would incur if
        you bought target‐size share sand the total income you would receive
        if you sold target‐size shares.""")
    parser.add_argument('--input',
                        help='File or stream to read data from. jfyi: You can pipe input as well.',
                        default=None,
                        required=False)
    parser.add_argument('--target‐size',
                        help='Desired target‐size shares count.',
                        default=None,
                        dest='target',
                        type=int,
                        required=True)
    parser.add_argument('--debug',
                        action="store_true",
                        help='Enable debug output',
                        default=False)

    ns = parser.parse_args()
    filename = ns.input
    debug = ns.debug
    target_size = ns.target

    if debug:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    # sanity validators
    try:
        if filename:
            filename = os.path.abspath(filename)
            if not os.path.exists(filename):
                raise ValidationError("File '%s' not found" % filename)

        if not target_size or target_size <= 0:
            raise ValidationError("Got '%s', but target‐size shares can't be less than 0" % target_size)

    except ValidationError as exp:
        die(str(exp))

    book = None

    if filename:
        logger.debug("Loading: '%s'..." % filename)
        book = BookAnalyzer.load(target_size=target_size, filename=filename)
    else:
        logger.debug("Reading data from input stream")
        book = BookAnalyzer(target_size=target_size)

    book.run()

    sys.exit(0)
