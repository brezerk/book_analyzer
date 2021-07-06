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

import unittest
import unittest.mock
import sys
import os
import io

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

# app imports

from core.book import BookAnalyzer


class TestMemoryDatabase(unittest.TestCase):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    maxDiff = None

    def setUp(self):
        pass

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_01_sample_small(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=200, filename=os.path.join(self.__location__, "data", "book_analyzer.small.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.small.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_02_sample_small_broken(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=200, filename=os.path.join(self.__location__, "data", "book_analyzer.small.broken.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.small.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_03_sample_200(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=200, filename=os.path.join(self.__location__, "data", "book_analyzer.200.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.200.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_04_sample_10000(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=200, filename=os.path.join(self.__location__, "data", "book_analyzer.10000.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.10000.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_05_full_1(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=1, filename=os.path.join(self.__location__, "data", "book_analyzer.full.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.full.1.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_06_full_200(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=200, filename=os.path.join(self.__location__, "data", "book_analyzer.full.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.full.200.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_07_full_10000(self, mock_stdout):
        """
        Test append with correct values
        """
        book = BookAnalyzer.load(target_size=10000, filename=os.path.join(self.__location__, "data", "book_analyzer.full.stdin"))
        book.run()
        with open(file=os.path.join(self.__location__, "data", "book_analyzer.full.10000.stdout"), mode='r') as ref:
            self.assertEqual(mock_stdout.getvalue(), ref.read())
