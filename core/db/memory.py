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
from core.db.base import BaseDatabase
from core.db.metadata import Metadata
from core.db.types.bookrow import BookRow
from core.logger import logger
from core.exceptions import FileLoadError


__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"


class MemoryDatabase(BaseDatabase):
    """
    In memory test database
    """
    def __init__(self):
        self.__storage = 'memory'
        self.__asks = Metadata(side=D_SIDE_ASK)
        self.__bids = Metadata(side=D_SIDE_BID)

    def add(self, row):
        # type: (BookRow) -> None
        side = row.get_side()
        if side == D_SIDE_ASK:
            self.__asks.append(row)
        elif side == D_SIDE_BID:
            self.__bids.append(row)
        else:
            logger.error("Unknown side '%s'", side)

    def remove(self, row):
        # type: (BookRow) -> None
        index = row.get_order_id()
        if self.__asks.has_index(index):
            self.__asks.delete(row)
        elif self.__bids.has_index(index):
            self.__bids.delete(row)
        else:
            logger.error("Order ID '%s' is not in the list. Skip.", index)

    def search(self, side, size):
        # type: (str, int) -> float
        amount = 0.0
        left_size = size
        if side == D_SIDE_ASK:
            if self.__asks.get_count() >= size:
                orders = self.__asks.get_orders()
                for order in orders:
                    order_price = order[0]
                    order_size = order[1]
                    if order_size >= left_size:
                        amount = amount + order_price * left_size
                        break
                    else:
                        amount = amount + order_price * order_size
                        left_size = left_size - order_size
                logger.debug("B %s [%s]" % (amount, self.__asks.get_orders()))
        elif side == D_SIDE_BID:
            if self.__bids.get_count() >= size:
                orders = self.__bids.get_orders()
                for order in orders:
                    order_price = order[0]
                    order_size = order[1]
                    if order_size >= left_size:
                        amount = amount + order_price * left_size
                        break
                    else:
                        amount = amount + order_price * order_size
                        left_size = left_size - order_size
                logger.debug("S %s [%s]" % (amount, self.__bids.get_orders()))
        else:
            logger.error("Unknown side '%s'", side)
        return amount

    def search_metadata(self, side, size):
        pass
