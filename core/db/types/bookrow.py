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
from core.exceptions import FileLoadError

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"


class BookRow(object):
    """
    BookRow class to be used with NoSQL DBs like redis or test memory db
    """
    def __init__(self, timestamp, order_id, side, price, size):
        # type: (int, str, str, float, int) -> None
        if not isinstance(timestamp, int) or timestamp <= 0:
            raise ValueError("Timestamp should be positive integer")
        self.__timestamp = timestamp
        if not isinstance(order_id, str) or not order_id:
            raise ValueError("Order id should be not empty string")
        self.__order_id = order_id
        if side not in [D_SIDE_ASK, D_SIDE_BID, None]:
            raise ValueError("Invalid side: %s" % side)
        self.__side = side
        if price:
            if not (isinstance(price, float) or isinstance(price, int)) or price <= 0:
                raise ValueError("Price should be positive double")
        if isinstance(price, int):
            self.__price = float(price)
        else:
            self.__price = price
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size should be positive integer")
        self.__size = size

    def get_timestamp(self):
        # type: () -> int
        return self.__timestamp

    def get_order_id(self):
        # type: () -> str
        return self.__order_id

    def get_side(self):
        # type: () -> str
        return self.__side

    def get_price(self):
        # type: () -> float
        return self.__price

    def get_size(self):
        # type: () -> int
        return self.__size
