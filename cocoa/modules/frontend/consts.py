# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

SearchType = Enum('BOOK', 'USER', 'GROUP', 'COLIST', 'POST')
SearchType.BOOK.set_text(_(u'Book'))
SearchType.USER.set_text(_(u'User'))
SearchType.GROUP.set_text(_(u'Group'))
SearchType.COLIST.set_text(_(u'Colist'))
SearchType.POST.set_text(_(u'Post'))
