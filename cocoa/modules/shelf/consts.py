# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

# 书架专栏
ColumnType = Enum('HAVE', 'READ', 'READING', 'WISH', 'LIKE')
ColumnType.HAVE.set_text(_(u'我有'))
ColumnType.READ.set_text(_(u'读过'))
ColumnType.READING.set_text(_(u'在读'))
ColumnType.WISH.set_text(_(u'想读'))
ColumnType.LIKE.set_text(_(u'喜欢'))
