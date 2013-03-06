# -*- coding: utf-8 -*-
from testcases import TestCase

from cocoa.extensions import db
from cocoa.modules.book.models import Book
from cocoa.modules.book.helpers import isbn10_to_13, isbn13_to_10

class TestBook(TestCase):

    def test_isbn_converter(self):
        isbn10 = '7531343762'
        assert isbn10_to_13(isbn10) == '9787531343769'

        isbn13 = '9787531343769'
        assert isbn13_to_10(isbn13) == '7531343762'
