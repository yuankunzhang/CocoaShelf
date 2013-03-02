# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

class UserConst(object):

    role = {
        'MEMBER':    (0, _('member')),
        'MODERATOR': (1, _(u'moderator')),
        'ADMIN': (2, _('admin')),
    }

    gender = {
        'SECRET': (0, _('secret')),
        'MALE':   (1, _('male')),
        'FEMALE': (2, _('female')),
    }
