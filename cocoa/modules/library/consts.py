# -*- coding: utf-8 -*-
from cocoa.helpers.enum import Enum

Shelf_type = Enum('HAVE', 'READ', 'READING', 'WISH', 'LIKE')
Shelf_type.HAVE.set_name('shelf_have')
Shelf_type.READ.set_name('shelf_read')
Shelf_type.READING.set_name('shelf_reading')
Shelf_type.WISH.set_name('shelf_wish')
Shelf_type.LIKE.set_name('shelf_like')
