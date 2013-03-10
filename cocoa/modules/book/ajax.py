# -*- coding: utf-8 -*-
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from cocoa.helpers.common import str2list
from .models import Book

class AjaxActions(object):

    @staticmethod
    def add_to_shelf(obj_response, book_id, shelf_columns,
                     str_tags=None, comment=None):
        """添加图书到书架"""

        if not current_user.is_authenticated():
            return

        book = Book.query.get_or_404(book_id)

        current_user.shelf.add_book_to_shelf(book, shelf_columns) 

        if str_tags is not None:
            current_user.add_booktags(book, str2list(str_tags))

        if comment is not None:
            pass

        obj_response.alert(_(u'Added to your shelf!'))
