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
        self.__asks = []
        self.__bids = []
        self.__asks_metadata = Metadata()
        self.__bids_metadata = Metadata()

    def insert(self, timestamp, order_id, side, price, size):
        # Type: (int, str, str, int, int) -> None
        row = BookRow(timestamp, order_id, price, size)
        if side == D_SIDE_ASK:
            self.__asks.append(row)
            self.__asks_metadata.append(row)
        elif side == D_SIDE_BID:
            self.__bids.append(row)
            self.__bids_metadata.append(row)
        else:
            logger.error("Unknown side '%s'", side)

    def delete(self, order_id, size):
        pass

    def search(self, side, size):
        pass

    def search_metadata(self, side, size):
        pass
