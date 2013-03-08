# -*- coding: utf-8 -*-
from cocoa.helpers.enum import Enum

ShelfType = Enum('HAVE', 'READ', 'READING', 'WISH', 'LIKE')
ShelfType.HAVE.set_text('shelf_have')
ShelfType.READ.set_text('shelf_read')
ShelfType.READING.set_text('shelf_reading')
ShelfType.WISH.set_text('shelf_wish')
ShelfType.LIKE.set_text('shelf_like')
