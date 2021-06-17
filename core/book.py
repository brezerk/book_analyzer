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

import os
import sys

# app imports
from core.defines import *
from core.db.memory import MemoryDatabase
from core.db.types.bookrow import BookRow
from core.logger import logger
from core.exceptions import FileLoadError

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

D_INPUT_TS = 0
D_INPUT_ACTION = 1
D_INPUT_ORDER_ID = 2

D_INPUT_A_SIDE = 3
D_INPUT_A_PRICE = 4
D_INPUT_A_SIZE = 5

D_INPUT_R_SIZE = 3


class BookAnalyzer:
    """
    Implements BookAnalyzer core logic

    Properties:
    """

    def __init__(self, target_size):
        # type: (int) -> None
        """
        Initialize the board and map
        Generate an board with random chars if x and y passed
        """
        self.__target_size = target_size
        self.__stream = sys.stdin
        self.__db = MemoryDatabase()
        self.__oef_term = False

        self.__last_bid = 0.0
        self.__last_ask = 0.0

    @classmethod
    def load(cls, target_size, filename):
        # type: (int, str) -> BookAnalyzer
        """
        Load board from csv file returns an class instance

        Keyword arguments:
            filename -- full path to the file
        """
        if not os.path.exists(filename):
            raise FileLoadError("File '%s' not found" % filename)

        instance = cls(target_size=target_size)
        instance.__stream = open(filename, mode='r')
        instance.__oef_term = True
        return instance

    def run(self):
        # type: () -> None
        """
        Read stream
        """
        try:
            buff = ''
            while True:
                line = self.__stream.readline().strip()
                if line:
                    self.parse(line)
                else:
                    if self.__oef_term:
                        break
        except KeyboardInterrupt:
            self.__stream.flush()
            pass

    def search(self, timestamp):
        # type: (int) -> None
        cost_ask = self.__db.search(D_SIDE_ASK, self.__target_size)
        if cost_ask != self.__last_ask:
            if cost_ask == 0.0:
                print("%s B NA" % timestamp)
            else:
                print("%s B %.2f" % (timestamp, cost_ask))
            self.__last_ask = cost_ask
        cost_bid = self.__db.search(D_SIDE_BID, self.__target_size)
        if cost_bid != self.__last_bid:
            if cost_bid == 0.0:
                print("%s S NA" % timestamp)
            else:
                print("%s S %.2f" % (timestamp, cost_bid))
            self.__last_bid = cost_bid

    def parse(self, line):
        # type: (str) -> None
        """
        Parse message and push data into database
        """
        args = line.split(" ")
        nargs = len(args)
        timestamp = int(args[D_INPUT_TS])
        if nargs < 4:
            logger.error("Invalid message length: '%s'. Skip" % line)
            return
        action = args[D_INPUT_ACTION]
        if action == D_ORDER_ADD:
            if nargs != 6:
                logger.error("Invalid message length: '%s'. Skip" % line)
                return
            self.__db.add(
                BookRow(
                    timestamp=int(args[D_INPUT_TS]),
                    order_id=args[D_INPUT_ORDER_ID],
                    side=args[D_INPUT_A_SIDE],
                    price=float(args[D_INPUT_A_PRICE]),
                    size=int(args[D_INPUT_A_SIZE])
                )
            )
        elif action == D_ORDER_REM:
            if nargs != 4:
                logger.error("Invalid message length: '%s'. Skip" % line)
                return
            self.__db.remove(
                BookRow(
                    timestamp=int(args[D_INPUT_TS]),
                    order_id=args[D_INPUT_ORDER_ID],
                    side="",
                    price=0.0,
                    size=int(args[D_INPUT_R_SIZE])
                )
            )
        else:
            logger.error("Invalid message (action): '%s'. Skip" % line)
        self.search(timestamp)
