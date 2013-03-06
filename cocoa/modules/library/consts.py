# -*- coding: utf-8 -*-
from cocoa.helpers.enum import Enum

Shelf_type = Enum('HAVE', 'READ', 'READING', 'WISH', 'LIKE')
Shelf_type.HAVE.set_text('shelf_have')
Shelf_type.READ.set_text('shelf_read')
Shelf_type.READING.set_text('shelf_reading')
Shelf_type.WISH.set_text('shelf_wish')
Shelf_type.LIKE.set_text('shelf_like')
