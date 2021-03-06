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

__author__ = "Oleksii S. Malakhov <brezerk@brezblock.org.ua>"
__license__ = "CC0"

# magic numbers!

D_COLOR = '\033[92m\033[1m'
D_COLOR_END = '\033[0m'

# Order action
D_ORDER_ADD = 'A'
D_ORDER_REM = 'R'

# Side
D_SIDE_ASK = 'S'
D_SIDE_BID = 'B'

# Input message args
D_INPUT_TS = 0
D_INPUT_ACTION = 1
D_INPUT_ORDER_ID = 2

D_INPUT_A_SIDE = 3
D_INPUT_A_PRICE = 4
D_INPUT_A_SIZE = 5

D_INPUT_R_SIZE = 3

D_INOUT_A_ARGS = 6
D_INOUT_R_ARGS = 4
