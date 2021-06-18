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
import os

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

# app imports

from core.db.memory import MemoryDatabase
from core.db.types.bookrow import BookRow
from core.defines import D_SIDE_ASK, D_SIDE_BID


class TestMemoryDatabase(unittest.TestCase):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def setUp(self):
        pass

    def test_e2e_01_valid(self):
        """
        Test append with correct values
        """
        db = MemoryDatabase()

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 0)

        db.add(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        db.add(BookRow(28800562, 'c', D_SIDE_BID, 44.10, 100))
        db.remove(BookRow(28800744, 'b', "", 0, 100))
        db.add(BookRow(28800538, 'd', D_SIDE_BID, 44.18, 157))
        db.add(BookRow(28800773, 'e', D_SIDE_ASK, 44.38, 100))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 8832.56)

        db.remove(BookRow(28800796, 'd', "", 0, 157))
        db.add(BookRow(28800812, 'f', D_SIDE_BID, 44.18, 157))
        db.add(BookRow(28800974, 'g', D_SIDE_ASK, 44.27, 100))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 8865.0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 8832.56)

        db.remove(BookRow(28800975, 'e', "", 0, 100))
        db.remove(BookRow(28812071, 'f', "", 0, 100))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 0)

    def test_e2e_01_valid_vs_invalid(self):
        """
        Test append with correct values
        """
        db = MemoryDatabase()

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 0)

        db.add(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        db.add(BookRow(28800562, 'c', D_SIDE_BID, 44.10, 100))
        db.add(BookRow(28800562, 'c', D_SIDE_BID, 0.10, 100))
        db.remove(BookRow(28800744, 'b', "", 0, 100))
        db.add(BookRow(28800538, 'd', D_SIDE_BID, 44.18, 157))
        db.add(BookRow(28800773, 'e', D_SIDE_ASK, 44.38, 100))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 8832.56)

        db.remove(BookRow(28800796, 'd', "", 0, 157))
        db.remove(BookRow(28800796, 'dxxx', "", 0, 157))
        db.add(BookRow(28800812, 'f', D_SIDE_BID, 44.18, 157))
        db.add(BookRow(28800974, 'g', D_SIDE_ASK, 44.27, 100))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 8865.0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 8832.56)

        db.remove(BookRow(28800975, 'e', "", 0, 100500))
        db.remove(BookRow(28812071, 'f', "", 0, 900))

        self.assertEqual(db.search(D_SIDE_ASK, 200), 0)
        self.assertEqual(db.search(D_SIDE_BID, 200), 0)
