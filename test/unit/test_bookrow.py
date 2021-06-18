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
from core.db.types.bookrow import BookRow
from core.defines import D_SIDE_ASK


class TestBookrow(unittest.TestCase):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def setUp(self):
        pass

    def test_init(self):
        """
        Test expected init vals
        """
        row = BookRow(100500, 'q', D_SIDE_ASK, 9000, 100)
        self.assertEqual(row.get_timestamp(), 100500)
        self.assertEqual(row.get_order_id(), 'q')
        self.assertEqual(row.get_side(), D_SIDE_ASK)
        self.assertEqual(row.get_price(), 9000)
        self.assertEqual(row.get_size(), 100)

    def test_init_raises(self):
        """
        Test expected init vals
        """
        with self.assertRaises(ValueError):
            row = BookRow("QUAKE", 'q', D_SIDE_ASK, 90.00, 100)
        with self.assertRaises(ValueError):
            row = BookRow(100500, 3, D_SIDE_ASK, 90.00, 100)
        with self.assertRaises(ValueError):
            row = BookRow(100500, 'q', "ARENA", 90.33, 100)
        with self.assertRaises(ValueError):
            row = BookRow(100500, 'q', D_SIDE_ASK, "RULEZ", 100)
        with self.assertRaises(ValueError):
            row = BookRow(100500, 'q', D_SIDE_ASK, 90.10, "Q3DM6")
