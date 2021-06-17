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

# app imports
from core.defines import *
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

    def __init__(self):
        self.__count = 0
        self.__index = []
        self.__orders = []

    def get_count(self):
        return self.__count

    def get_orders(self):
        return self.__orders

    def get_index(self):
        return self.__index

    def get_order(self, order_id):
        # Type: str -> List[int, int]
        index = self.__index.index(order_id)
        return self.__orders[index]

    def append(self, row):
        # Type: BookRow -> None
        """
        Inject row data into metadata DB
        """
        order_id = row.get_order_id()
        if order_id in self.__index:
            logger.error("'%s' already in the list. Skipping." % (order_id))
            return
        price = row.get_price()
        self.__count = self.__count + row.get_size()

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
        # Type: BookRow -> None
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
