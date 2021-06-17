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

from typing import List, Union, Any

# app imports
from core.defines import *
from core.db.types.bookrow import BookRow
from core.logger import logger

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

D_ORDER_PRICE = 0
D_ORDER_SIZE = 1


class Metadata(object):
    """
    Metadata class

    this calss represent some kind of first level cache for overall
    calls count.

    It is designed to reduce DB calls in excange of additional memory usage.
    """

    def __init__(self, side=D_SIDE_ASK):
        # type: (str) -> None
        self.__count = 0
        self.__index = []  # type: List[str]
        self.__orders = []  # type: List[List[Any]]
        self.__side = side

    def get_count(self):
        # type: () -> int
        return self.__count

    def get_orders(self):
        # type: () -> List[List[Any]]
        return self.__orders

    def get_index(self):
        # type: () -> List[str]
        return self.__index

    def has_index(self, index):
        # type: (str) -> bool
        return index in self.__index

    def get_order(self, order_id):
        # type: (str) -> List[Any]
        index = self.__index.index(order_id)
        return self.__orders[index]

    def append(self, row):
        # type: (BookRow) -> None
        """
        Inject row data into metadata DB
        """
        order_id = row.get_order_id()
        if order_id in self.__index:
            logger.error("'%s' already in the list. Skipping." % (order_id))
            return
        self.__count = self.__count + row.get_size()

        if self.__side == D_SIDE_ASK:
            self.append_ask(row)
        elif self.__side == D_SIDE_BID:
            self.append_bid(row)
        else:
            logger.error("Unknown side '%s'", self.__side)

    def append_bid(self, row):
        # type: (BookRow) -> None
        """
        Inject row data into metadata DB for BID
        """
        order_id = row.get_order_id()
        price = row.get_price()
        i = 0
        # no, don't use enumirate on large arrays :)
        for order in self.__orders:
            if order[D_ORDER_PRICE] <= price:
                self.__index.insert(i, order_id)
                self.__orders.insert(
                    i,
                    [
                        price,
                        row.get_size()
                    ])
                injected = True
                return
            i += 1

        # pushback
        self.__index.append(order_id)
        self.__orders.append(
            [
                price,
                row.get_size()
            ]
        )

    def append_ask(self, row):
        # type: (BookRow) -> None
        """
        Inject row data into metadata DB for ASK
        """
        order_id = row.get_order_id()
        price = row.get_price()
        i = 0
        # no, don't use enumirate on large arrays :)
        for order in self.__orders:
            if order[D_ORDER_PRICE] >= price:
                self.__index.insert(i, order_id)
                self.__orders.insert(
                    i,
                    [
                        price,
                        row.get_size()
                    ])
                injected = True
                return
            i += 1

        # pushback
        self.__index.append(order_id)
        self.__orders.append(
            [
                price,
                row.get_size()
            ]
        )

    def delete(self, row):
        # type: (BookRow) -> None
        """
        Reduces size of order on specified amount (removes order if <= 0)
        """
        order_id = row.get_order_id()
        index = -1
        try:
            index = self.__index.index(order_id)
        except ValueError:
            logger.error("'%s' not found in the list. Skipping." % (order_id))
            return
        size = row.get_size()
        size_recorded = self.__orders[index][D_ORDER_SIZE]
        if size_recorded <= size:
            del self.__orders[index]
            self.__count = self.__count - size_recorded
            self.__index.remove(order_id)
        else:
            self.__orders[index][D_ORDER_SIZE] = size_recorded - size
            self.__count = self.__count - size
        if self.__count < 0:
            self.__count = 0
