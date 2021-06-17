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

from core.db.metadata import Metadata
from core.db.types.bookrow import BookRow
from core.defines import D_SIDE_ASK, D_SIDE_BID


class TestMetadata(unittest.TestCase):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def setUp(self):
        pass

    def test_init(self):
        """
        Test expected init vals
        """
        metadata = Metadata()
        self.assertEqual(metadata.get_count(), 0)
        self.assertEqual(metadata.get_orders(), [])
        self.assertEqual(metadata.get_index(), [])

    def test_append_correct_ask(self):
        """
        Test append with correct values
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        self.assertEqual(metadata.get_count(), 100)
        self.assertEqual(metadata.get_orders(), [[44.26, 100]])
        self.assertEqual(metadata.get_index(), ['b'])
        self.assertEqual(metadata.has_index('b'), True)
        metadata.append(BookRow(28800633, 'c', D_SIDE_ASK, 14.26, 50))
        self.assertEqual(metadata.get_count(), 150)
        self.assertEqual(metadata.get_orders(), [[14.26, 50], [44.26, 100]])
        self.assertEqual(metadata.get_index(), ['c', 'b'])
        self.assertEqual(metadata.has_index('c'), True)
        self.assertEqual(metadata.has_index('b'), True)
        metadata.append(BookRow(28800833, 'z', D_SIDE_ASK, 74.00, 10))
        self.assertEqual(metadata.get_count(), 160)
        self.assertEqual(metadata.get_orders(), [[14.26, 50], [44.26, 100], [74.00, 10]])
        self.assertEqual(metadata.get_index(), ['c', 'b', 'z'])
        self.assertEqual(metadata.has_index('c'), True)
        self.assertEqual(metadata.has_index('b'), True)
        self.assertEqual(metadata.has_index('z'), True)

    def test_append_correct_bid(self):
        """
        Test append with correct values
        """
        metadata = Metadata(side=D_SIDE_BID)
        metadata.append(BookRow(28800538, 'b', D_SIDE_BID, 44.26, 100))
        self.assertEqual(metadata.get_count(), 100)
        self.assertEqual(metadata.get_orders(), [[44.26, 100]])
        self.assertEqual(metadata.get_index(), ['b'])
        self.assertEqual(metadata.has_index('b'), True)
        metadata.append(BookRow(28800633, 'c', D_SIDE_BID, 14.26, 50))
        self.assertEqual(metadata.get_count(), 150)
        self.assertEqual(metadata.get_orders(), [[44.26, 100], [14.26, 50]])
        self.assertEqual(metadata.get_index(), ['b', 'c'])
        self.assertEqual(metadata.has_index('c'), True)
        self.assertEqual(metadata.has_index('b'), True)
        metadata.append(BookRow(28800833, 'z', D_SIDE_BID, 74.00, 10))
        self.assertEqual(metadata.get_count(), 160)
        self.assertEqual(metadata.get_orders(), [[74.00, 10], [44.26, 100], [14.26, 50]])
        self.assertEqual(metadata.get_index(), ['z', 'b', 'c'])
        self.assertEqual(metadata.has_index('c'), True)

    def test_append_dups(self):
        """
        Test append with dups
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        self.assertEqual(metadata.get_count(), 100)
        self.assertEqual(metadata.get_orders(), [[44.26, 100]])
        self.assertEqual(metadata.get_index(), ['b'])
        metadata.append(BookRow(28800633, 'b', D_SIDE_ASK, 14.26, 50))
        self.assertEqual(metadata.get_count(), 100)
        self.assertEqual(metadata.get_orders(), [[44.26, 100]])
        self.assertEqual(metadata.get_index(), ['b'])

    def test_delete_correct(self):
        """
        Test deleteing correct values
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        metadata.append(BookRow(28800633, 'c', D_SIDE_ASK, 14.26, 50))
        metadata.append(BookRow(28800833, 'z', D_SIDE_ASK, 74.00, 10))
        self.assertEqual(metadata.get_index(), ['c', 'b', 'z'])
        metadata.delete(BookRow(28800633, 'b', D_SIDE_ASK, None, 100))
        self.assertEqual(metadata.get_count(), 60)
        self.assertEqual(metadata.get_orders(), [[14.26, 50], [74.00, 10]])
        self.assertEqual(metadata.get_index(), ['c', 'z'])
        metadata.delete(BookRow(28800633, 'c', D_SIDE_ASK, None, 10))
        self.assertEqual(metadata.get_count(), 50)
        self.assertEqual(metadata.get_orders(), [[14.26, 40], [74.00, 10]])
        self.assertEqual(metadata.get_index(), ['c', 'z'])

    def test_delete_invalid(self):
        """
        Test deleteing correct values
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800633, 'c', D_SIDE_ASK, 14.26, 50))
        metadata.append(BookRow(28800833, 'z', D_SIDE_ASK, 74.00, 10))
        self.assertEqual(metadata.get_index(), ['c', 'z'])
        metadata.delete(BookRow(28800633, 'x', D_SIDE_ASK, None, 100))
        self.assertEqual(metadata.get_count(), 60)
        self.assertEqual(metadata.get_orders(), [[14.26, 50], [74.00, 10]])
        self.assertEqual(metadata.get_index(), ['c', 'z'])
        metadata.delete(BookRow(28800633, 'c', D_SIDE_ASK, None, 100500))
        self.assertEqual(metadata.get_count(), 10)
        self.assertEqual(metadata.get_orders(), [[74.00, 10]])
        self.assertEqual(metadata.get_index(), ['z'])
        self.assertEqual(metadata.has_index('q'), False)
        self.assertEqual(metadata.has_index('t'), False)
        self.assertEqual(metadata.has_index('za'), False)

    def test_append_get_order_correct(self):
        """
        Test append with correct values
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        metadata.append(BookRow(28800633, 'c', D_SIDE_ASK, 14.26, 50))
        metadata.append(BookRow(28800833, 'z', D_SIDE_ASK, 74.00, 10))
        self.assertEqual(metadata.get_count(), 160)

        self.assertEqual(metadata.get_order('c'), [14.26, 50])
        self.assertEqual(metadata.get_order('b'), [44.26, 100])
        self.assertEqual(metadata.get_order('z'), [74.00, 10])

    def test_append_get_order_incorrect(self):
        """
        Test append with correct values
        """
        metadata = Metadata(side=D_SIDE_ASK)
        metadata.append(BookRow(28800538, 'b', D_SIDE_ASK, 44.26, 100))
        metadata.append(BookRow(28800633, 'c', D_SIDE_ASK, 14.26, 50))
        metadata.append(BookRow(28800833, 'z', D_SIDE_ASK, 74.00, 10))
        self.assertEqual(metadata.get_count(), 160)

        with self.assertRaises(ValueError):
            metadata.get_order('u')

        with self.assertRaises(ValueError):
            metadata.get_order(100500)
