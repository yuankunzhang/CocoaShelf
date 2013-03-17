# -*- coding: utf-8 -*-
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from ..book.models import Book
from ..follower.models import Follower

class AjaxActions(object):

    @staticmethod
    @login_required
    def finish_reading(obj_response, book_id):
        book = Book.query.get_or_404(book_id)
        current_user.shelf.finish_reading(book)

        obj_response.alert(_(u'Finish reading a book.'))

    @staticmethod
    @login_required
    def follow(obj_response, user_id):
        from ..account.models import User

        user = User.query.get_or_404(user_id)
        f = Follower(user, current_user)
        f.save()

        obj_response.alert(_(u'You followed this user.'))
