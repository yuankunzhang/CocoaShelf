# -*- coding: utf-8 -*-
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from ..book.models import Book

class AjaxActions(object):

    @staticmethod
    @login_required
    def finish_reading(obj_response, book_id):

        book = Book.query.get_or_404(book_id)

        current_user.shelf.finish_reading(book)

        obj_response.alert(_(u'Finish reading a book.'))
