# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

PostType = Enum('ARTICAL', 'REVIEW', 'NOTE')
PostType.ARTICAL.set_text(_(u'Article'))
PostType.REVIEW.set_text(_(u'Review'))
PostType.NOTE.set_text(_(u'Note'))

PostStatus = Enum('DRAFT', 'PUBLISHED', 'DROPPED')
PostStatus.DRAFT.set_text('Draft')
PostStatus.PUBLISHED.set_text('Published')
PostStatus.DROPPED.set_text('Dropped')
